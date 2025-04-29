from insightface.app import FaceAnalysis

# 初始化 ArcFace 模型（需单独安装 insightface）
app = FaceAnalysis(name="arcface_r100_v1", providers=["CUDAExecutionProvider"])
app.prepare(ctx_id=0)

def extract_embedding(image, bbox):
    x1, y1, x2, y2 = bbox
    face_img = image[y1:y2, x1:x2]
    face = app.get(face_img)[0]
    return face["embedding"]
