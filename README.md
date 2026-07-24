# 🤚 HandSpeak — Gesture-to-Voice Recognition (I Love Minji)

Real-time hand gesture recognition app built with **MediaPipe Tasks API (HandLandmarker)** and **OpenCV**, using a single hand to trigger different spoken words based on which finger touches the thumb.

## 💡 Inspiration

This project was inspired by a TikTok video of **Minji (NewJeans)**, where she tried out a hand gesture-to-voice recognition demo. After watching it, I got curious about how that kind of tech actually works — so I decided to build my own version from scratch using MediaPipe and OpenCV, and learn the whole pipeline along the way (hand landmark detection, gesture logic, and audio playback).

<img width="739" height="765" alt="WhatsApp Image 2026-07-24 at 18 48 35 (1)" src="https://github.com/user-attachments/assets/75d920f7-c3ba-4391-b687-79a678782e58" />
<img width="1336" height="828" alt="WhatsApp Image 2026-07-24 at 22 31 05" src="https://github.com/user-attachments/assets/42abeec0-a37a-4bbe-a67d-4c8da01faaea" />

## ✨ How It Works

Using 21 hand landmarks detected in real time from a webcam feed, the app measures the distance between the thumb tip and each fingertip (normalized by hand size, so it works at any distance from the camera). When a finger touches the thumb, the app plays the matching audio clip and displays the word live on screen.

| Gesture (👍 touches...) | Label Shown | Sound Played |
|---|---|---|
| ☝️ Index finger | **I** | `i.mp3` |
| 🖕 Middle finger | **LOVE** | `love.mp3` |
| 💍 Ring finger | **MINJI** | `minji.mp3` |

All three labels are displayed live above each fingertip, turning red when an active touch/gesture is detected.

## 🛠️ Tech Stack

- **Python 3.12**
- **MediaPipe Tasks API** — `HandLandmarker` for 21-point hand landmark detection
- **OpenCV** — webcam capture & real-time rendering
- **Pygame** — audio playback

## 📁 Project Structure

```
kode_tangan_minji_love_nius/
├── main.py                     # Main application
├── model/
│   └── hand_landmarker.task    # MediaPipe hand landmark model
├── suara/
│   ├── i.mp3
│   ├── love.mp3
│   └── minji.mp3
├── assets/
├── requirements.txt
└── README.md
```

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/<username>/<repo-name>.git
cd <repo-name>
```

### 2. Create and activate a virtual environment (Python 3.12 recommended)
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Download the hand landmark model
Download `hand_landmarker.task` from the official MediaPipe model page and place it in `model/`:
```
https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task
```

### 5. Run the app
```bash
python main.py
```

Press **Q** to quit.

## ⚙️ Configuration

Adjust sensitivity and behavior at the top of `main.py`:
- `TOUCH_THRESHOLD` — how close fingers need to be to count as "touching" (lower = stricter)
- `COOLDOWN` — minimum seconds between repeated triggers of the same sound

## 📌 Notes

- Audio files (`i.mp3`, `love.mp3`, `minji.mp3`) are not included in this repo for privacy/size reasons — add your own recordings to `suara/` with matching filenames.
- Requires a working webcam.

## 📄 License

This project is for personal/portfolio use.
