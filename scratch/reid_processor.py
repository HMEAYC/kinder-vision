import json
import os
import math

def calculate_distance(v1, v2):
    """計算兩個特徵向量之間的歐幾里得距離"""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))

def process_video_analytics(video_name, detected_features_list, raw_metrics_list):
    # 1. 載入身分特徵資料庫
    db_path = "/Users/roverchen/Documents/Apps/kinder-vision/memory/identity_features.db.json"
    with open(db_path, 'r') as f:
        db = json.load(f)
    
    identities = db['identities']
    results = []

    # 2. 遍歷偵測到的幼兒
    for i, detected_feat in enumerate(detected_features_list):
        matched_id = None
        min_dist = float('inf')
        
        # 與資料庫比對
        for identity in identities:
            dist = calculate_distance(detected_feat, identity['features']['face_embedding_sample'])
            if dist < 0.5:  # 門檻值：距離越小越相似
                if dist < min_dist:
                    min_dist = dist
                    matched_id = identity
        
        # 3. 判定身分
        if matched_id:
            status = "returning"
            student_id = matched_id['student_id']
            name_code = matched_id['display_name']
        else:
            status = "new"
            student_id = f"S_NEW_{len(results) + 1}"
            name_code = f"Child_New_{len(results) + 1}"

        # 4. 封裝指標數據
        metrics_entry = {
            "student_id": student_id,
            "name_code": name_code,
            "session_date": "2026-05-05",
            "video_ref": video_name,
            "status": status,
            "metrics": raw_metrics_list[i]
        }
        
        # 5. 自動寫入 memory 目錄
        output_path = f"/Users/roverchen/Documents/Apps/kinder-vision/memory/2026-05-05_{student_id}_metrics.json"
        with open(output_path, 'w') as out_f:
            json.dump(metrics_entry, out_f, indent=2, ensure_ascii=False)
        
        results.append(name_code)
        print(f"✅ 已完成歸戶：{name_code} (Status: {status}, Dist: {min_dist if matched_id else 'N/A'})")

    return results

# --- 模擬運行 ---
if __name__ == "__main__":
    # 模擬從 W4-6 影片偵測到的三個人
    # 1. 小明 (特徵與 DB 接近)
    # 2. 小 A (特徵與 DB 接近)
    # 3. 新同學 (特徵完全不同)
    mock_detected_features = [
        [0.89, 0.11, -0.21, 0.46, 0.68, -0.04, 0.15, 0.54], # 很像小明
        [0.13, -0.44, 0.77, 0.22, -0.10, 0.88, 0.04, -0.31], # 很像小 A
        [0.99, 0.99, 0.99, 0.99, 0.99, 0.99, 0.99, 0.99]     # 完全是新人
    ]
    
    mock_metrics = [
        {"rhythmic_sync": {"avg_error_ms": 38}, "inhibitory_control": {"max_displacement_cm": 6.2}},
        {"rhythmic_sync": {"avg_error_ms": 24}, "inhibitory_control": {"max_displacement_cm": 2.1}},
        {"rhythmic_sync": {"avg_error_ms": 150}, "inhibitory_control": {"max_displacement_cm": 20.0}}
    ]

    print("🚀 啟動 Kinder Vision 自動歸戶處理器...")
    process_video_analytics("W4-6 Musical Movement.MOV", mock_detected_features, mock_metrics)
