import cv2
import time
import math
import os
import pygame
import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision

# ---------- KONFIGURASI ----------
MODEL_PATH = "model/hand_landmarker.task"
SOUND_FOLDER = "suara"

# Mapping: jari yang nyentuh jempol -> nama file suara (tanpa .mp3)
GESTURES = {
    8:  "i",       # telunjuk + jempol
    12: "love",    # tengah   + jempol
    16: "minji",   # manis    + jempol
}

# Label yang ditampilkan di atas tiap ujung jari
FINGER_LABELS = {
    8:  "I",
    12: "LOVE",
    16: "MINJI",
}

TOUCH_THRESHOLD = 0.45   # rasio jarak / ukuran tangan, makin kecil = harus makin nempel
COOLDOWN = 1.2           # detik, jeda minimal sebelum suara yang sama bisa bunyi lagi

# ---------- SETUP AUDIO ----------
pygame.mixer.init()
sounds = {}
for finger_id, name in GESTURES.items():
    path = os.path.join(SOUND_FOLDER, f"{name}.mp3")
    if os.path.exists(path):
        sounds[name] = pygame.mixer.Sound(path)
    else:
        print(f"[WARNING] File suara belum ada: {path}")

def play_sound(name):
    if name in sounds:
        sounds[name].play()
    else:
        print(f"[SKIP] Suara '{name}' belum tersedia, taruh file {name}.mp3 di folder suara/")

# ---------- SETUP HAND LANDMARKER ----------
base_options = mp_python.BaseOptions(model_asset_path=MODEL_PATH)
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO,
    num_hands=1,
    min_hand_detection_confidence=0.6,
    min_hand_presence_confidence=0.6,
    min_tracking_confidence=0.6,
)
landmarker = vision.HandLandmarker.create_from_options(options)

# ---------- HELPER ----------
def distance(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)

last_played_time = {name: 0.0 for name in GESTURES.values()}
current_word = ""
current_word_until = 0

# ---------- KAMERA ----------
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Kamera tidak bisa dibuka. Cek index kamera atau izin akses.")
    exit()

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

    timestamp_ms = int(time.time() * 1000)
    result = landmarker.detect_for_video(mp_image, timestamp_ms)

    h, w, _ = frame.shape

    if result.hand_landmarks:
        hand = result.hand_landmarks[0]

        # ukuran tangan sebagai referensi normalisasi (wrist -> pangkal jari tengah)
        wrist = hand[0]
        middle_mcp = hand[9]
        hand_size = distance(wrist, middle_mcp)
        if hand_size == 0:
            hand_size = 1e-6

        thumb_tip = hand[4]

        # gambar semua titik landmark
        for lm in hand:
            cx, cy = int(lm.x * w), int(lm.y * h)
            cv2.circle(frame, (cx, cy), 4, (0, 255, 0), -1)

        # cek tiap jari terhadap jempol + gambar label di atas tiap jari
        for finger_id, name in GESTURES.items():
            finger_tip = hand[finger_id]
            d = distance(thumb_tip, finger_tip) / hand_size

            tip_x, tip_y = int(finger_tip.x * w), int(finger_tip.y * h)
            is_touching = d < TOUCH_THRESHOLD

            # warna label: merah kalau lagi nempel ke jempol, putih kalau nggak
            label_color = (0, 0, 255) if is_touching else (255, 255, 255)
            label = FINGER_LABELS[finger_id]

            # posisi teks: di atas ujung jari, tengah-kan sesuai lebar teks
            text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
            text_x = tip_x - text_size[0] // 2
            text_y = tip_y - 25

            cv2.putText(frame, label, (text_x, text_y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, label_color, 2, cv2.LINE_AA)

            if is_touching:
                cv2.circle(frame, (tip_x, tip_y), 12, (0, 0, 255), 3)
                now = time.time()
                if now - last_played_time[name] > COOLDOWN:
                    play_sound(name)
                    last_played_time[name] = now
                    current_word = name.upper()
                    current_word_until = now + 1.0

    # tampilkan kata yang lagi aktif
    if time.time() < current_word_until:
        cv2.putText(frame, current_word, (30, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 200, 255), 4)

    cv2.imshow("Kode Tangan Minji Love Nius", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
landmarker.close()