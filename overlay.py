import cv2
import keyboard
import numpy as np
from PIL import Image
import obsws_python as obs
import easyocr
import os
from dotenv import load_dotenv

from config import (
    DEVICE_ID, NAME_REGION, POKEMON_REGIONS,
    OUTPUT_POKEMON,
    OBS_NAME_SOURCE, OBS_POKEMON_SOURCE,
    HOTKEY_CAPTURE, HOTKEY_CLEAR,
    OCR_LANGUAGES,
)

load_dotenv()

client = obs.ReqClient(host="localhost", port=4455, password=os.getenv("OBS_PASSWORD"))

cap = cv2.VideoCapture(DEVICE_ID, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

print("OCRモデルを読み込み中...")
reader = easyocr.Reader(OCR_LANGUAGES, gpu=False)
print("OCRモデル読み込み完了")


def crop(frame, region):
    x1, y1, x2, y2 = region
    return frame[y1:y2, x1:x2]


def ocr_name(img_bgr):
    results = reader.readtext(img_bgr)
    return ' '.join([r[1] for r in results]) if results else ''


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


def refresh_obs_image(source_name, filepath):
    abs_path = os.path.abspath(filepath)
    client.set_input_settings(name=source_name, settings={"file": abs_path}, overlay=True)


def capture():
    ret, frame = cap.read()
    if not ret:
        print("キャプチャ失敗")
        return

    name_text = ocr_name(crop(frame, NAME_REGION))
    client.set_input_settings(name=OBS_NAME_SOURCE, settings={"text": name_text}, overlay=True)
    print(f"名前: {name_text}")

    process_pokemon(frame).save(OUTPUT_POKEMON)
    refresh_obs_image(OBS_POKEMON_SOURCE, OUTPUT_POKEMON)

    print("キャプチャ完了")


def clear():
    client.set_input_settings(name=OBS_NAME_SOURCE, settings={"text": ""}, overlay=True)
    blank = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
    blank.save(OUTPUT_POKEMON)
    refresh_obs_image(OBS_POKEMON_SOURCE, OUTPUT_POKEMON)
    print("クリア完了")


keyboard.add_hotkey(HOTKEY_CAPTURE, capture)
keyboard.add_hotkey(HOTKEY_CLEAR, clear)

print(f"起動完了 | {HOTKEY_CAPTURE}: キャプチャ | {HOTKEY_CLEAR}: クリア | Esc: 終了")
keyboard.wait("esc")

cap.release()
client.disconnect()
