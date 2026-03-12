import cv2
from ultralytics import YOLO

model = YOLO("best.pt")

url = "http://192.168.1.4"

cap = cv2.VideoCapture(url)

while True:
    ret, frame = cap.read()

    if not ret:
        print("Frame not received")
        break

    results = model(frame)

    annotated = results[0].plot()

    cv2.imshow("Detection", annotated)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()