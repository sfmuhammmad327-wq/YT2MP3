# YT2MP3
# 🎵 YT to MP3 | NextGen Converter

A modern, lightning-fast YouTube to MP3 converter featuring a sleek glassmorphism UI, real-time download progress tracking, and an automated Google OAuth2 bypass to reliably defeat YouTube's anti-bot algorithms.

Created by **Sai The Limit**.

---

## ✨ Features

* **Anti-Bot Bypass (OAuth2):** Utilizes `pytubefix` with Google Device flow to authenticate as a trusted device, permanently bypassing YouTube's strict 403/PO Token blocks.
* **Real-Time Progress Tracking:** Asynchronous backend threading communicates with the frontend to display a live, glowing progress bar for both downloading and encoding phases.
* **High-Fidelity Audio:** Bypasses basic library conversions by directly piping raw audio streams into local **FFmpeg** engines for flawless, selectable bitrate encoding (128k to 320k).
* **Glassmorphism UI:** A fully responsive, animated, premium user interface built with pure HTML/CSS/JS.
* **Auto-Cleanup:** Automatically deletes raw temporary streams to save hard drive space after successful conversions.

---

## 🛠️ Prerequisites

Before you can run this app, your system needs two things:

1. **Python 3.8+** installed on your machine.
2. **FFmpeg** installed and added to your system's `PATH`. 
   * *Windows:* Download from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/), extract, and add the `bin` folder to your Environment Variables.
   * *Mac:* `brew install ffmpeg`
   * *Linux:* `sudo apt install ffmpeg`

---

## 🚀 Installation & Setup

**1. Clone the repository**
```bash
git clone [https://github.com/sfmuhammmad327-wq/YT2MP3.git](https://github.com/sfmuhammmad327-wq/YT2MP3.git)
cd YT2MP3
```
**2. Install required Python packages**

```Bash
pip install flask flask-cors pytubefix
```

## 🎮 How to Use
**1. Start the Backend Server**
Open your terminal in the project folder and run:

```Bash
python yt2mp3.py
```

**2. Open the UI**
Simply double-click the ytmp3.html file to open it in any modern web browser.

**3. The First-Time Setup (Crucial)**
Because this app uses official OAuth2 to bypass YouTube's bot detection, you must authorize it once.

Paste a YouTube link into the UI and click Convert Now.

Look at your Python terminal. It will pause and ask you to visit https://www.google.com/device and enter a code.

Open the link, log into your YouTube/Google account, and enter the code.

Press Enter in your terminal. The download will resume instantly.


Note: A secure tokens.json file is now cached locally. You will not have to do this again.



## 👤 Author
Muhammad Saiffuddin (SAI THE LIMIT)

GitHub: @sfmuhammmad327-wq

UI Design, Backend Architecture, and Network Routing.

Disclaimer: This tool is for educational purposes and personal archiving only. Please respect YouTube's Terms of Service and copyright laws.
