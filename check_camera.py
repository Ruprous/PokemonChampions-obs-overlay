import cv2
from config import DEVICE_ID

cap = cv2.VideoCapture(DEVICE_ID, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
print(f"デバイス {DEVICE_ID} を表示中... Qキーで終了")

while True:
    ret, frame = cap.read()
    if not ret:
        print("映像取得失敗")
        break
    cv2.imshow(f"Device {DEVICE_ID}", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
