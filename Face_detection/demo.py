import os
import cv2
import numpy as np
from Face_detection.Feature_extraction import extract_embedding
from Face_detection.data_load import extract_frames
from Face_detection.detection import detect_faces

# 完整流程示例
video_path = "input.mp4"
output_dir = "frames"
extract_frames(video_path, output_dir, fps=5)

# 遍历帧并处理
face_data = []
for frame_file in os.listdir(output_dir):
    frame = cv2.imread(os.path.join(output_dir, frame_file))
    faces = detect_faces(frame)
    for bbox in faces:
        embedding = extract_embedding(frame, bbox)
        face_data.append({"bbox": bbox, "embedding": embedding})

# 构建 FAISS 索引
embeddings = np.array([d["embedding"] for d in face_data])
index = faiss.IndexFlatL2(512)
index.add(embeddings)
