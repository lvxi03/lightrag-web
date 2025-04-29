import faiss
import numpy as np

# 创建 FAISS 索引
index = faiss.IndexFlatIP(512)  # 内积加速
embeddings = np.load("face_embeddings.npy").astype(np.float32)
faiss.normalize_L2(embeddings)  # 归一化便于内积计算
index.add(embeddings)

# 检索 Top-5 相似结果
def search(query_embedding, top_k=5):
    query_embedding = query_embedding.astype(np.float32)
    faiss.normalize_L2(query_embedding)
    distances, indices = index.search(query_embedding, top_k)
    return indices[0]
