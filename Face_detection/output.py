# 生成 JSON 结果
def format_result(indices, timestamps, bboxes):
    return [
        {"timestamp": timestamps[i], "bbox": bboxes[i], "similarity": 0.95}
        for i in indices
    ]
