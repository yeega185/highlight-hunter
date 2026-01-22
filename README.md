# 🎮 Highlight Hunter: AI-Powered Gaming Clipper

**Highlight Hunter** is an automated video highlight extraction pipeline designed for FPS games (specifically **Apex Legends**). It leverages **Multimodal AI** to analyze gameplay footage and automatically clip exciting moments.

**Highlight Hunter** 是一個針對 FPS 遊戲（如 **Apex Legends**）設計的自動化精華剪輯系統。它整合了 **多模態 AI (Multimodal AI)** 技術，能自動分析遊戲畫面與語音，精準捕捉並剪輯出精彩時刻。

> **Current Status:** Week 2 Complete (Audio & Vision Integration) 🚀

---

## ✨ Key Features (核心功能)

* **🎧 Dual-Engine Analysis (雙引擎分析)**
    * **Audio (Local):** Uses **OpenAI Whisper** to detect voice comms (e.g., "Cracked", "Knocked").
        * *語音分析：使用本地端 Whisper 模型辨識語音溝通（如：「破甲」、「倒地」）。*
    * **👁️ Vision (Cloud):** Uses **Google Gemini 2.5 Flash** to understand visual context and kill feeds.
        * *視覺分析：使用雲端 Gemini 2.5 辨識畫面中的擊殺資訊與戰鬥場景。*
* **✂️ Smart Clipping (智慧剪輯)**
    * Automatically calculates buffer times (start/end) to ensure context is preserved using **MoviePy**.
    * *自動計算前後緩衝時間，確保剪輯片段的完整性。*
* **🔒 Security First (資安優先)**
    * API keys are managed via environment variables (`.env`), ensuring no sensitive data is leaked.
    * *API 金鑰透過環境變數管理，確保資安無虞。*

---

## 🛠️ Tech Stack (技術堆疊)

* **Language**: Python 3.12+
* **AI Models**:
    * `openai-whisper` (Medium model)
    * `google-generativeai` (Gemini 2.5 Flash)
* **Media Processing**: `moviepy`, `ffmpeg-python`
* **Tools**: PowerShell, Git

---

## 📂 Project Structure (專案結構)

```text
highlight-hunter/
├── .env                  # API Keys (⚠️ Not uploaded / 請勿上傳)
├── .gitignore            # Git configuration
├── README.md             # Documentation
├── data/
│   ├── in/               # Raw videos (原始影片)
│   └── highlights/       # Generated clips (產出精華)
├── out/                  # JSON Logs (分析紀錄)
└── scripts/
    ├── highlight_hunter_v1.py    # Whisper-based analysis
    ├── test_gemini_vision.py     # Gemini Vision-based analysis
    ├── w2d4_integration_test.py  # Clipping logic (MoviePy)
    └── extract_audio.ps1         # Utility tools
```
---
## 🚀 Getting Started

* **1.Installation (安裝)**
Clone the repository and install dependencies:

```bash
git clone [https://github.com/Yeega185/highlight-hunter.git](https://github.com/Yeega185/highlight-hunter.git)
cd highlight-hunter
pip install -U openai-whisper moviepy google-generativeai python-dotenv
```

* **2. Configuration (設定)**
Create a .env file in the root directory to store your Google Gemini API Key. 請在根目錄建立 .env 檔案並填入你的 API Key：

```bash
GEMINI_API_KEY=your_actual_api_key_here
```

* **3. Usage (使用說明)**
Option A: Audio-Based Extraction (Whisper 語音分析)
Analyzes voice commands to find highlights.

```bash
python scripts/highlight_hunter_v1.py
```
Option B: Vision-Based Extraction (Gemini 視覺分析)
Uses computer vision to identify kills and intense moments
```bash
python scripts/test_gemini_vision.py
```
Option C: Generate Clips (開始剪輯)
Reads the generated JSON analysis and cuts the video files.

```bash
python scripts/w2d4_integration_test.py
```
---

## 📊 Output Format (輸出格式)
The pipeline generates JSON logs to ensure traceability. 系統會產出標準化的 JSON 格式，方便追蹤與除錯。

Example (out/sample_transcript.json):
```bash
{
    "project": "highlight-hunter",
    "file_name": "sample.mp4",
    "transcript": [
        {
            "start": 106.85,
            "end": 108.92,
            "text": "Enemy cracked! (對面紅甲)"
        },
        {
            "start": 145.20,
            "end": 150.00,
            "text": "One down! (倒一個)"
        }
    ]
}
```
---

## 🗺️ Roadmap (開發路線圖)
[o] Week 1: Environment Setup & FFmpeg Audio Extraction.

[o] Week 2: AI Transcription (Whisper) & Vision Analysis (Gemini).

[ ] Week 3: LLM Context Understanding (Filtering non-highlights).

[ ] Week 4: Automated Video Montage Assembly.

Created by Yeega - 2026