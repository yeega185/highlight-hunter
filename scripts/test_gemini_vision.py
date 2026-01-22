import google.generativeai as genai
import time
import os
import json
from dotenv import load_dotenv  # [新增] 匯入 dotenv 工具

# 1. 載入保險箱 (這行會去讀取 .env 檔案)
load_dotenv()

# 2. 從環境變數抓取 Key
api_key = os.getenv("GEMINI_API_KEY")

# 3. 檢查有沒有抓到 (安全防護)
if not api_key:
    raise ValueError("❌ 找不到 API Key！請確認你有建立 .env 檔案並填寫 GEMINI_API_KEY")

# 4. 配置 API (使用抓到的變數)
genai.configure(api_key=api_key, transport="rest")


def analyze_video_with_gemini(video_path):
    print(f"🎬 啟動最強 Gemini 2.5 多模態分析：{os.path.basename(video_path)}")

    # 2. 更新模型名稱 (對齊你剛才診斷出的清單)
    model = genai.GenerativeModel('gemini-2.5-flash')

    # 3. 上傳影片
    video_file = genai.upload_file(path=video_path)
    print(f"⏳ 影片上傳中，等待處理...")

    while video_file.state.name == "PROCESSING":
        time.sleep(5)
        video_file = genai.get_file(video_file.name)

    # 4. Prompt 工程 (這裡不變)
    prompt = """
    你是一位專業的 Apex Legends 賽評。請分析這段影片，並找出所有精彩時刻。
    包含：破甲、擊倒、精彩走位。
    請只回傳 JSON 格式：[{"start": 秒數, "end": 秒數, "reason": "描述"}]
    """

    # 5. 獲取結果
    response = model.generate_content([prompt, video_file])

    # 清理並讀取 JSON
    clean_json = response.text.replace(
        '```json', '').replace('```', '').strip()
    return json.loads(clean_json)


if __name__ == "__main__":
    test_video = "data/in/sample.mp4"
    try:
        highlights = analyze_video_with_gemini(test_video)
        print("\n✨ Gemini 2.5 產出的精華清單：")
        print(json.dumps(highlights, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"❌ 執行出錯：{e}")
