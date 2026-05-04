# Kinder Vision 幼兒行為分析系統

基於論文《解碼教室裡的舞蹈：AI 如何看懂孩子的肢體學習語言》設計，結合電腦視覺與音樂教育心理學的輔助分析系統。

## 核心分析技術 (Core Analytics Technologies)

### 1. 節奏同步度分析 (Rhythmic Synchronization)
- **技術**：`librosa` (音訊強拍偵測) + **MediaPipe Holistic** (肢體位移峰值偵測)。
- **原理**：將肢體動作（如跳躍、拍手）的峰值時間與音樂強拍進行毫秒級比對。
- **指標**：計算平均誤差 (ms)，評估幼兒的節奏感與對音樂信號的反應延遲。

### 2. 抑制控制分析 (Inhibitory Control)
- **技術**：音訊能量衰減偵測 (Audio Stop Signal) + 持續性位移追蹤。
- **原理**：自動識別音樂停止瞬間，並捕捉幼兒在隨後 1 秒內的身體座標變化。
- **指標**：累積位移量 (cm)。位移愈小，代表幼兒的衝動控制與自我調節能力愈強。

### 3. 動作流暢度分析 (Movement Fluency)
- **技術**：**Jerk Analysis (加加速度分析)**。
- **原理**：計算肢體運動加速度的變化率。
- **指標**：平均 Jerk 值 (m/s³)。流暢的動作具有穩定的加速度變化（低 Jerk），而僵硬或遲疑的動作則會產生劇烈的數值波動。

### 4. 個別追蹤軌跡 (Individual Trajectory)
- **技術**：**YOLOv8** + **ByteTrack** (多目標追蹤) + 透視投影轉換。
- **原理**：將監視器視角映射為教室 3D 平面座標，分析幼兒的移動路徑。
- **指標**：探索廣度、社交距離與移動速度變異，視覺化幼兒在空間中的參與程度。

## 技術棧 (Technology Stack)
- **Macro 分析**：YOLOv8-Pose (群體追蹤、隊形偵測)
- **Micro 分析**：MediaPipe Holistic (個體精細動作、表情與手指追蹤)
- **多目標追蹤**：ByteTrack
- **音訊處理**：librosa (BPM 與靜音偵測)

### 5. 人像資料庫與個案追蹤 (Face Database & ID Link)
- **技術**：**InsightFace** (特徵向量提取) + **Person Re-identification (ReID)**。
- **原理**：將幼兒臉部特徵轉化為去識別化的特徵向量（Embedding），實現跨時段數據歸戶。
- **指標**：跨日成長趨勢、個案動作流暢度改善曲線。

### 6. LLM 增強型教育建議 (LLM-Enhanced Advisor)
- **技術**：Large Language Model (LLM) 數據翻譯引擎。
- **原理**：將微觀與巨觀數據（如誤差 ms、位移 cm）轉譯為富有教育意義且具溫度的自然語言報告。
- **指標**：班級整體亮點、個案進步見證、具體家庭互動建議。

## 技術棧 (Technology Stack)
- **Macro 分析**：YOLOv8-Pose (群體追蹤、隊形偵測)
- **Micro 分析**：MediaPipe Holistic (個體精細動作)
- **身分識別**：InsightFace / ArcFace (ReID & Edge Recovery)
- **報告生成**：LLM-Enhanced Generator
- **音訊處理**：librosa (BPM 與靜音偵測)

## 系統技術總結 (v2.1 Summary)

### 1. 核心願景與定位
Kinder Vision 是一套結合 **電腦視覺 (Computer Vision)** 與 **教育心理學** 的 AI 輔助系統。其核心價值在於將原本難以量化的「幼兒音樂律動表現」，轉化為具備科學證據的「長期成長軌跡」。

### 2. 關鍵技術突破：個案追蹤與 ReID
系統從「單次匿名分析」演進為「具備記憶能力的追蹤系統」：
- **Identity Manager (身分中樞)**：利用 **InsightFace** 提取特徵向量，建立身分資料庫。
- **自動化歸戶邏輯**：透過歐幾里得距離計算，自動識別回流幼兒或標註新生。
- **環境邊緣化補償**：整合了外觀 ReID 與時空預測，解決了遮蔽或中斷問題。

### 3. 三大指標分析引擎
- **Rhythmic Sync**：毫秒級動作誤差量化。
- **Inhibitory Control**：測量靜止穩定度（位移 cm），評估衝動調節能力。
- **Movement Fluency**：應用 **Jerk Analysis** 評估肢體發育協調性。

### 4. LLM 增強型教育溝通
- **數據故事化**：將指標轉化為富有溫度的家長聯絡簿文字。
- **進步見證**：自動比對歷史存檔，生成成長趨勢報告。

---
*最後更新：2026-05-05 | 技術開發：Antigravity AI*


