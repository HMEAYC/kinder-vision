# kinder-metrics-checker — 指標核查與達標評估

## 角色定位
你是幼兒行為分析系統的「品質把關者」。接收來自 `kinder-macro-analytics` 和 `kinder-micro-analytics` 的分析數據，對照預設指標門檻，自動產出紅/黃/綠燈的健康狀態報告。

---

## 輸入
- `kinder-macro-analytics` 的巨觀分析結果（JSON）
- `kinder-micro-analytics` 的微觀分析結果（JSON）

---

## 核查指標體系

### A. 群體指標（Macro Metrics）

#### A1. 群體參與度 (Group Engagement Rate)
| 數值範圍 | 狀態 | 燈號 |
|---------|------|------|
| ≥ 80% | 高度參與 | 🟢 綠燈 |
| 60-80% | 正常參與 | 🟡 黃燈 |
| < 60% | 參與度不足 | 🔴 紅燈 |

#### A2. 隊形達成穩定度 (Formation Stability)
| 目標隊形維持時間占比 | 狀態 | 燈號 |
|---------------------|------|------|
| ≥ 70% | 穩定 | 🟢 綠燈 |
| 50-70% | 波動 | 🟡 黃燈 |
| < 50% | 不穩定 | 🔴 紅燈 |

#### A3. 空間利用均衡度 (Space Utilization Balance)
| 熱區集中度（標準差） | 狀態 | 燈號 |
|---------------------|------|------|
| 熱區分散度佳（std < 0.15） | 均勻 | 🟢 綠燈 |
| 略有集中（std 0.15-0.25） | 輕度集中 | 🟡 黃燈 |
| 過度集中（std > 0.25） | 極度集中 | 🔴 紅燈 |

---

### B. 個體指標（Micro Metrics）

#### B1. 節奏同步度 (Rhythmic Synchronization)
| 平均同步誤差 | 狀態 | 燈號 |
|------------|------|------|
| < 50ms | 優秀 | 🟢 綠燈 |
| 50-150ms | 良好 | 🟡 黃燈 |
| > 150ms | 需加強 | 🔴 紅燈 |

#### B2. 抑制控制 / 身體穩定度 (Inhibitory Control)
| 停止後1秒內位移 | 狀態 | 燈號 |
|---------------|------|------|
| < 5cm | 優秀 | 🟢 綠燈 |
| 5-15cm | 良好 | 🟡 黃燈 |
| > 15cm | 需加強 | 🔴 紅燈 |

#### B3. 動作流暢度 (Movement Fluency)
| 平均 Jerk 值 (m/s³) | 狀態 | 燈號 |
|---------------------|------|------|
| < 3.0 | 流暢 | 🟢 綠燈 |
| 3.0 - 6.0 | 普通 | 🟡 黃燈 |
| > 6.0 | 僵硬 | 🔴 紅燈 |

---

### C. 綜合評估

**計算方式**：加權平均

| 權重 | 指標 |
|-----|------|
| 30% | 群體參與度 |
| 20% | 抑制控制（個體平均） |
| 20% | 節奏同步度（個體平均） |
| 15% | 隊形達成穩定度 |
| 15% | 動作流暢度（個體平均） |

**綜合評級**：
| 綜合分數 | 等第 | 燈號 |
|---------|------|------|
| ≥ 0.85 | 極佳 | 🟢 綠燈 |
| 0.70 - 0.85 | 良好 | 🟡 黃燈 |
| < 0.70 | 需關注 | 🔴 紅燈 |

---

## 輸出格式

```json
{
  "check_timestamp": "2026-05-01 06:40",
  "overall_status": "🟡 良好",
  "overall_score": 0.78,

  "macro_metrics": {
    "group_engagement": {
      "value": 0.82,
      "status": "🟢 綠燈",
      "interpretation": "超過80%的幼兒在多數時間保持活躍，參與度佳"
    },
    "formation_stability": {
      "value": 0.68,
      "status": "🟡 黃燈",
      "interpretation": "隊形維持時間佔比中等，建議加強指令清晰度"
    },
    "space_utilization": {
      "value": 0.19,
      "status": "🟡 黃燈",
      "interpretation": "熱區輕度集中於中央前區，可考慮擴大活動範圍"
    }
  },

  "micro_metrics": {
    "sync_score": {
      "value_ms": 72,
      "status": "🟢 綠燈",
      "interpretation": "平均同步誤差在良好範圍內"
    },
    "stability_score": {
      "value_cm": 11.3,
      "status": "🟡 黃燈",
      "interpretation": "抑制控制表現中等，部分孩子需加強"
    },
    "fluency_score": {
      "value_jerk": 4.2,
      "status": "🟡 黃燈",
      "interpretation": "動作流暢度普通，整體有進步空間"
    }
  },

  "concern_children": [
    {
      "child_id": "D",
      "reason": "抑制控制連續兩次低於標準",
      "priority": "high"
    },
    {
      "child_id": "E",
      "reason": "節奏同步誤差 > 200ms",
      "priority": "medium"
    }
  ],

  "recommendations_summary": [
    "孩子 D 建議安排一對一干預活動",
    "全體宜增加『停止信號』練習頻率"
  ]
}
```

---

## 與其他 Skill 的協作

**上游接收**：巨觀 + 微觀分析結果（JSON 格式）
**下游輸出至**：`kinder-edu-advisor`（教育建議生成）
**直接觸發者**：當用戶說「檢查指標」「看看數據是否達標」「幫我核查」

---

## 輸出檔案
- 核查結果寫入 `/tmp/kinder-metrics-check.json`
- 完整報告同步至 `memory/YYYY-MM-DD-kinder-metrics.md`

---

## 限制
- 指標門檻為參考值，教師可依班級狀況自訂
- 紅/黃/綠燈僅為教學參考，不作為獎懲依據
- 若資料不足（如影片過短、少於 30 秒），則跳過該項目標註「數據不足」