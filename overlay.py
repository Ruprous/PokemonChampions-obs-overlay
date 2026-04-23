import cv2
import keyboard
import numpy as np
from PIL import Image
import obsws_python as obs
import os
from dotenv import load_dotenv

from config import (
    DEVICE_ID, NAME_REGION, POKEMON_REGIONS,
    OUTPUT_NAME, OUTPUT_POKEMON,
    OBS_NAME_SOURCE, OBS_POKEMON_SOURCE,
    HOTKEY_CAPTURE, HOTKEY_CLEAR,
)

load_dotenv()

client = obs.ReqClient(host="localhost", port=4455, password=os.getenv("OBS_PASSWORD"))

cap = cv2.VideoCapture(DEVICE_ID, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)


def crop(frame, region):
    x1, y1, x2, y2 = region
    return frame[y1:y2, x1:x2]


def process_name(img_bgr):
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    rgba = np.zeros((gray.shape[0], gray.shape[1], 4), dtype=np.uint8)
    rgba[:, :, 0] = 255
    rgba[:, :, 1] = 255
    rgba[:, :, 2] = 255
    rgba[:, :, 3] = mask
    return Image.fromarray(rgba, "RGBA")


def process_pokemon(frame):
    slots = [crop(frame, r) for r in POKEMON_REGIONS]
    margin = 20
    h = max(s.shape[0] for s in slots)
    w_total = sum(s.shape[1] for s in slots) + margin * (len(slots) - 1)
    combined = np.zeros((h, w_total, 4), dtype=np.uint8)
    x = 0
    for s in slots:
        rgb = cv2.cvtColor(s, cv2.COLOR_BGR2RGB)
        combined[:s.shape[0], x:x + s.shape[1], :3] = rgb
        combined[:s.shape[0], x:x + s.shape[1], 3] = 255
        x += s.shape[1] + margin
    return Image.fromarray(combined, "RGBA")


def refresh_obs(source_name, filepath):
    abs_path = os.path.abspath(filepath)
    client.set_input_settings(name=source_name, settings={"file": abs_path}, overlay=True)


def capture():
    ret, frame = cap.read()
    if not ret:
        print("キャプチャ失敗")
        return

    process_name(crop(frame, NAME_REGION)).save(OUTPUT_NAME)
    refresh_obs(OBS_NAME_SOURCE, OUTPUT_NAME)

    process_pokemon(frame).save(OUTPUT_POKEMON)
    refresh_obs(OBS_POKEMON_SOURCE, OUTPUT_POKEMON)

    print("キャプチャ完了")


def clear():
    blank = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
    blank.save(OUTPUT_NAME)
    blank.save(OUTPUT_POKEMON)
    refresh_obs(OBS_NAME_SOURCE, OUTPUT_NAME)
    refresh_obs(OBS_POKEMON_SOURCE, OUTPUT_POKEMON)
    print("クリア完了")


keyboard.add_hotkey(HOTKEY_CAPTURE, capture)
keyboard.add_hotkey(HOTKEY_CLEAR, clear)

print(f"起動完了 | {HOTKEY_CAPTURE}: キャプチャ | {HOTKEY_CLEAR}: クリア | Esc: 終了")
keyboard.wait("esc")

cap.release()
client.disconnect()
