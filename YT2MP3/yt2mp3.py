from flask import Flask, request, send_file, jsonify, make_response
from flask_cors import CORS
from pytubefix import YouTube
import os
import uuid
from datetime import datetime
import urllib.parse
import re
import traceback
import subprocess
import threading
import sys
import logging

app = Flask(__name__)
CORS(app)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

DOWNLOAD_DIR = "temp_downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

tasks = {}

def process_video(task_id, url, chosen_bitrate):
    # 1. Lock the UI into the orange warning state
    tasks[task_id]['status'] = 'authenticating'
    
    try:
        def on_progress(stream, chunk, bytes_remaining):
            # Safe calculation in case YouTube hides the file size
            total_size = stream.filesize
            if total_size and total_size > 0:
                bytes_downloaded = total_size - bytes_remaining
                percentage = int((bytes_downloaded / total_size) * 85)
            else:
                percentage = 0
                
            tasks[task_id]['progress'] = percentage
            
            # THE FIX: .ljust(65) pads the end of the line with spaces,
            # acting as a physical eraser to prevent text overlapping!
            status_text = f"\r⚡ [{task_id[:8]}] Downloading... {percentage}%"
            sys.stdout.write(status_text.ljust(65))
            sys.stdout.flush()

        yt = YouTube(
            url, 
            use_oauth=True, 
            allow_oauth_cache=True,
            on_progress_callback=on_progress
        )
        
        # pytubefix pauses execution on this line. 
        # The UI will stay locked on the orange 'authenticating' warning until you hit Enter!
        raw_title = yt.title 
        
        # 2. Connection successful! Now we switch the UI back to blue.
        tasks[task_id]['status'] = 'downloading'
        
        tasks[task_id]['title'] = raw_title
        print(f"\n🎯 [{task_id[:8]}] Video Found: {raw_title}")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_title = re.sub(r'[\\/*?:"<>|]', "", raw_title).strip().replace(" ", "_")
        final_filename = f"{safe_title}_{chosen_bitrate}k-{timestamp}.mp3"
        tasks[task_id]['filename'] = final_filename
        
        raw_file_path = os.path.join(DOWNLOAD_DIR, f"{task_id}_raw")
        mp3_file_path = os.path.join(DOWNLOAD_DIR, f"{task_id}.mp3")
        tasks[task_id]['file_path'] = mp3_file_path
        
        audio_stream = yt.streams.get_audio_only()
        downloaded_raw_file = audio_stream.download(
            output_path=DOWNLOAD_DIR,
            filename=f"{task_id}_raw"
        )
        
        tasks[task_id]['status'] = 'converting'
        tasks[task_id]['progress'] = 90
        
        # Apply the eraser fix here too, so it cleanly wipes away the 85% download text
        encode_text = f"\r⚙️  [{task_id[:8]}] Extracting Audio & Encoding to MP3..."
        sys.stdout.write(encode_text.ljust(65))
        sys.stdout.flush()
        
        subprocess.run([
            'ffmpeg', 
            '-i', downloaded_raw_file, 
            '-vn', 
            '-b:a', f'{chosen_bitrate}k', 
            '-loglevel', 'quiet',
            '-y', 
            mp3_file_path
        ], check=True)
        
        if os.path.exists(downloaded_raw_file):
            os.remove(downloaded_raw_file)
            
        tasks[task_id]['status'] = 'completed'
        tasks[task_id]['progress'] = 100
        print(f"\n✅ [{task_id[:8]}] Conversion Complete! Ready for user download.")
        
    except Exception as e:
        traceback.print_exc()
        tasks[task_id]['status'] = 'error'
        tasks[task_id]['error'] = str(e)
        print(f"\n❌ [{task_id[:8]}] Error: {str(e)}")

@app.route('/convert', methods=['POST'])
def start_conversion():
    data = request.json
    url = data.get('url')
    chosen_bitrate = data.get('bitrate', '320')
    
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    task_id = str(uuid.uuid4())
    tasks[task_id] = {'progress': 0, 'status': 'starting', 'title': '', 'error': ''}
    
    thread = threading.Thread(target=process_video, args=(task_id, url, chosen_bitrate))
    thread.start()
    
    return jsonify({"task_id": task_id})

@app.route('/status/<task_id>', methods=['GET'])
def get_status(task_id):
    task = tasks.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task)

@app.route('/download/<task_id>', methods=['GET'])
def download_file(task_id):
    task = tasks.get(task_id)
    if not task or task['status'] != 'completed':
        return "File not ready", 400
        
    response = make_response(send_file(
        task['file_path'],
        as_attachment=True,
        download_name=task['filename']
    ))
    
    response.headers['X-Video-Title'] = urllib.parse.quote(task['title'])
    response.headers['Access-Control-Expose-Headers'] = 'X-Video-Title, Content-Disposition'
    return response

if __name__ == '__main__':
    app.run(debug=True, port=5000)