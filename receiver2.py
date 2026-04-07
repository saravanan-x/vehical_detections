import cv2
import requests
from ultralytics import YOLO

ESP_IP = "192.168.1.3"
stream_url = f"http://{ESP_IP}:80"

model = YOLO("best.pt")


cap = cv2.VideoCapture(stream_url)

if not cap.isOpened():
    print("ERROR: Cannot open ESP32 stream")
    exit()

cv2.namedWindow("ESP32 YOLO Detection", cv2.WINDOW_NORMAL)

# Set window size (WIDTH, HEIGHT)
cv2.resizeWindow("ESP32 YOLO Detection", 1200, 800)


while True:

    ret, frame = cap.read()

    if not ret:
        print("Frame not received")
        continue

    #  Rotate frame (fix orientation)
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

    results = model(frame, conf=0.25)

    large_object = False

    for r in results:
        if r.boxes is None:
            continue

        for box in r.boxes:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            area = (x2 - x1) * (y2 - y1)

            if area > 50000:   # adjust threshold if needed
                large_object = True

    try:
        if large_object:
            requests.get(f"http://{ESP_IP}/buzzer_on", timeout=0.1)
        else:
            requests.get(f"http://{ESP_IP}/buzzer_off", timeout=0.1)
    except:
        pass

 
    annotated = results[0].plot()

    cv2.imshow("ESP32 YOLO Detection", annotated)

    # Press ESC to exit
    if cv2.waitKey(1) & 0xFF == 27:
        break

# -----------------------------
# Cleanup
# -----------------------------
cap.release()
cv2.destroyAllWindows()