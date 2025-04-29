from ultralytics import YOLO

model = YOLO("./yolov11n-face.pt")  # 加载预训练模型

def detect_faces(image):
    results = model(image)
    faces = []
    for box in results[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
        faces.append((x1, y1, x2, y2))
    return faces
