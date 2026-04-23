import cv2

print("カメラデバイスを探し中...")
for i in range(10):
    cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            print(f"デバイス {i}: 映像あり ({int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))}x{int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))})")
        else:
            print(f"デバイス {i}: 開けたけど映像なし")
        cap.release()
    else:
        print(f"デバイス {i}: なし")
