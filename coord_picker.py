import cv2
from config import DEVICE_ID

cap = cv2.VideoCapture(DEVICE_ID, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

regions = []
state = {'pos': (0, 0), 'p1': None}

def on_mouse(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        param['pos'] = (x, y)
    if event == cv2.EVENT_LBUTTONDOWN:
        if param['p1'] is None:
            param['p1'] = (x, y)
            print(f"1点目: ({x}, {y})  → 次に2点目をクリック")
        else:
            x1, y1 = param['p1']
            x2, y2 = x, y
            region = (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))
            regions.append(region)
            print(f"領域{len(regions)} 確定: 左上({region[0]}, {region[1]}) 右下({region[2]}, {region[3]}) サイズ({region[2]-region[0]}x{region[3]-region[1]})")
            param['p1'] = None

cv2.namedWindow("Coord Picker")
cv2.setMouseCallback("Coord Picker", on_mouse, state)

print("1クリック目=左上、2クリック目=右下で領域確定 / Qで終了")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    display = frame.copy()
    x, y = state['pos']

    # 確定済み領域を描画
    for i, (x1, y1, x2, y2) in enumerate(regions):
        cv2.rectangle(display, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.putText(display, f"#{i+1}", (x1 + 4, y1 + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # 1点目確定済みならプレビュー矩形を描画
    if state['p1'] is not None:
        px, py = state['p1']
        cv2.rectangle(display, (px, py), (x, y), (0, 255, 0), 2)
        cv2.circle(display, (px, py), 5, (0, 255, 0), -1)

    # カーソルと座標表示
    cv2.drawMarker(display, (x, y), (0, 255, 0), cv2.MARKER_CROSS, 20, 2)
    cv2.putText(display, f"({x}, {y})", (x + 10, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow("Coord Picker", display)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

if regions:
    print("\n確定した領域一覧:")
    for i, (x1, y1, x2, y2) in enumerate(regions):
        print(f"  #{i+1}: 左上({x1}, {y1}) 右下({x2}, {y2}) サイズ({x2-x1}x{y2-y1})")
