import cv2
import torch
from PIL import Image
import playsound

model = torch.hub.load("ultralytics/yolov5", "custom", path="fire.pt")



stream_url = "http://192.168.1.26:81/stream"


cap = cv2.VideoCapture(stream_url)


if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()


while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Could not read frame.")
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_pil = Image.fromarray(frame_rgb)
    results = model(frame_pil)
    detections = results.pandas().xyxy[0]
    for _, detection in detections.iterrows():
        x1, y1, x2, y2 = int(detection['xmin']), int(detection['ymin']), int(detection['xmax']), int(detection['ymax'])
        label = detection['name']
        confidence = detection['confidence']

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, f'{label} {confidence:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        playsound('fire_detected.mp3')
        with open("code_gsm.py") as f:
            exec(f.read())


    cv2.imshow("Stream View", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
