# kinder-micro-analytics — 微觀層個體動作分析

## 角色定位
你是幼兒行為分析系統的「微觀觀察員」。專注於分析**個別幼兒**的肢體動作細節，幫助教師理解每位孩子的動作學習歷程與行為特質。

---

## 輸入
- 來自 `kinder-vision-core` 指定的分析片段
- 或用戶直接要求針對「孩子 A」或「表現最不穩定的 3 位」進行深度分析
- 需指定：影片路徑、感興趣的時間區間、追蹤人數

---

## 分析維度

### 1. 節奏同步度分析 (Rhythmic Synchronization)
**目標**：測量每位幼兒的動作與音樂節拍之間的時間誤差。

**處理流程**：
1. 擷取音樂的 BPM（可用 librosa 或音訊分析工具）
2. 擷取幼兒關鍵動作時間點（拍手、踏步——以手腕/腳踝關鍵點位移峰值判定）
3. 計算每次動作與最近音樂強拍（Beat）的時間差

**同步誤差分級**：
| 同步誤差範圍 | 評級 | 說明 |
|------------|------|------|
| < 50ms | 優秀 | 動作與音樂高度吻合 |
| 50-150ms | 良好 | 節奏感佳，些微提前或落後 |
| 150-300ms | 需加強 | 明顯與音樂脫節 |
| > 300ms | 落後 | 大幅落後或提前，需特別關注 |

**輸出格式**：
```
{
  "child_id": "A",
  "bpm": 120,
  "synchronization_errors": [
    {"beat_time": "00:05.2", "action_time": "00:05.24", "error_ms": 40},
    {"beat_time": "00:06.7", "action_time": "00:06.68", "error_ms": -20},
    ...
  ],
  "avg_error_ms": 48,
  "sync_rating": "優秀"
}
```

---

### 2. 抑制控制分析 (Inhibitory Control — Stop Signal)
**目標**：測量孩子在「音樂停止」後身體是否能立刻靜止並保持穩定。

**處理流程**：
1. 偵測音訊中靜音段的起始點（Audio Stop Signal）
2. 擷取「靜止後 0.5s / 1.0s / 2.0s」三個時間點的身體關鍵點坐標
3. 計算相對於「停止前 0.5s」的位移量

**穩定度評級**：
| 停止後位移（1秒內） | 評級 |
|-------------------|------|
| < 5cm | 優秀 |
| 5-15cm | 良好 |
| 15-30cm | 需加強 |
| > 30cm | 明顯不穩定 |

**輸出格式**：
```
{
  "child_id": "B",
  "stop_signals_detected": [
    {"signal_time": "00:45.0", "displacement_cm": 3.2},
    {"signal_time": "01:32.5", "displacement_cm": 18.1},
    {"signal_time": "02:15.0", "displacement_cm": 8.7}
  ],
  "avg_displacement_cm": 10.0,
  "stability_rating": "需加強",
  "concern_flag": true
}
```

---

### 3. 動作流暢度分析 (Movement Fluency)
**目標**：評估動作是否自然、連貫，無僵硬或卡顿。

**處理流程**：
1. 取手腕/腳踝關鍵點的位移時間序列
2. 計算「Jerk」（加速度的變化率，即加加速度）
3. Jerk 越低 = 動作越平滑

**流暢度評級**：
| 平均 Jerk 值 (m/s³) | 評級 |
|---------------------|------|
| < 2.0 | 流暢 |
| 2.0 - 5.0 | 普通 |
| 5.0 - 10.0 | 僵硬 |
| > 10.0 | 非常僵硬 |

**輸出格式**：
```
{
  "child_id": "C",
  "body_parts": {
    "right_wrist": {"avg_jerk": 3.2, "rating": "普通"},
    "left_wrist": {"avg_jerk": 2.8, "rating": "普通"},
    "right_ankle": {"avg_jerk": 4.1, "rating": "普通"},
    "left_ankle": {"avg_jerk": 3.9, "rating": "普通"}
  },
  "overall_fluency": "普通"
}
```

---

### 4. 個別追蹤軌跡 (Individual Trajectory)
**目標**：針對教師指定或系統判定需要關注的幼兒，重建其課堂移動軌跡。

**處理流程**：
1. 使用 ByteTrack 或類似追蹤演算法對單一幼兒建立 ID
2. 擷取其所有幀的 (x, y) 位置
3. 繪製軌跡圖（Trajectory Plot）

**輸出格式**：
```
{
  "child_id": "D",
  "total_distance_cm": 1245,
  "avg_speed_cm/s": 6.8,
  "max_speed_cm/s": 28.3,
  "time_in_central_zone": 0.45,  // 45%時間在教室中央
  "trajectory_image": "/tmp/kinder-child-D-trajectory.png",
  "movement_pattern": "高探索型"  // 與中央區域相對
}
```

---

## 與其他 Skill 的協作

**上游觸發者**：`kinder-vision-core`（Step 3）
**下游輸出至**：`kinder-metrics-checker`（Step 4）、`kinder-edu-advisor`（Step 5）

**輸出檔案**：
- 結果寫入 `/tmp/kinder-micro-result.json`
- 軌跡圖寫入 `/tmp/kinder-child-{ID}-trajectory.png`
- 完整報告同步至 `memory/YYYY-MM-DD-kinder-micro.md`

---

## 限制
- 本 Skill 需要較高準確度的姿勢預測模型（MediaPipe Holistic 或 equivalent）
- 離線分析（課後）以確保準確度，不建議用於即時回饋
- 若偵測到多位幼兒重疊（遮蔽），軌跡可能中斷，需標注「追蹤丟失」時間點