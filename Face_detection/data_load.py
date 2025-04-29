import cv2

# 视频抽帧（每秒抽5帧）
def extract_frames(video_path, output_dir, fps=5):
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret: break
        if frame_count % int(cap.get(cv2.CAP_PROP_FPS) / fps) == 0:
            resized_frame = cv2.resize(frame, (640, 640))
            cv2.imwrite(f"{output_dir}/frame_{frame_count}.jpg", resized_frame)
        frame_count += 1
