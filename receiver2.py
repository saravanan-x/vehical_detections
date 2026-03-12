import cv2
import requests
from ultralytics import YOLO

# ESP32 IP
ESP_IP = "192.168.1.4"

# Load YOLO model
model = YOLO("best.pt")

# Camera stream
stream_url = f"http://{ESP_IP}:80"

cap = cv2.VideoCapture(stream_url)

if not cap.isOpened():
    print("ERROR: Cannot open ESP32 stream")
    exit()

while True:

    ret, frame = cap.read()

    if not ret:
        print("Frame not received")
        continue

    # Run YOLO detection
    results = model(frame, conf=0.25)

    large_object = False

    for r in results:
        if r.boxes is None:
            continue

        for box in r.boxes:

            # convert tensor to numbers
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()

            area = (x2 - x1) * (y2 - y1)

            if area > 50000:   # adjust threshold if needed
                large_object = True

    # Control buzzer
    try:
        if large_object:
            requests.get(f"http://{ESP_IP}/buzzer_on", timeout=0.1)
        else:
            requests.get(f"http://{ESP_IP}/buzzer_off", timeout=0.1)
    except:
        pass

    # Draw detections
    annotated = results[0].plot()

    cv2.imshow("ESP32 YOLO Detection", annotated)

    # Press ESC to exit
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()