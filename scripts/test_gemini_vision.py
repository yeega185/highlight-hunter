import google.generativeai as genai
import time
import os
import json
from dotenv import load_dotenv

# 1. 載入保險箱 (這行確保你的 Key 安全)
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ 錯誤：找不到 API Key！請確認你已經建立了 .env 檔案。")
    exit(1)

genai.configure(api_key=api_key, transport="rest")


def analyze_video_with_gemini(video_path):
    video_name = os.path.basename(video_path)
    print(f"\n🎬 [Pro 版] 啟動戰術分析：{video_name}")

    # 2. 升級模型：從 Flash 換成 Pro (大腦升級)
    # Pro 模型能看懂畫面上的小字 (如傷害數值)
    model = genai.GenerativeModel('gemini-flash-latest')

    print(f"⏳ 影片上傳中 (Pro 模型分析需要較多時間，請耐心等候)...")
    video_file = genai.upload_file(path=video_path)

    # 等待 Google 處理影片
    while video_file.state.name == "PROCESSING":
        print(".", end="", flush=True)
        time.sleep(5)
        video_file = genai.get_file(video_file.name)

    if video_file.state.name == "FAILED":
        print("\n❌ 影片處理失敗，請檢查格式或網路。")
        return

    print("\n🚀 AI 正在進行深度視覺分析 (尋找擊殺與破甲)...")

    # 3. 升級 Prompt：教它看細節 (Visual Cues)
    prompt = """
    你是 Apex Legends 的頂級戰術分析師。請逐秒分析這段影片，找出「高光時刻」。

    請特別注意畫面中的以下視覺特徵 (Visual Cues)：
    1. **擊倒資訊 (Kill Feed)**：畫面右上角是否出現綠色或紅色的擊倒/擊殺通知？
    2. **傷害數字 (Damage Numbers)**：畫面中央是否跳出大額傷害數字（如 100+）或紅色數字（代表破甲/碎甲）？
    3. **護甲破碎聲效/圖示**：是否有聽到清脆的玻璃破碎聲或看到敵人的護甲圖示破裂？
    4. **鳳凰治療**：玩家是否正在使用「鳳凰包」或「大電」補血？

    請只輸出符合上述特徵的片段，並嚴格排除單純在跑步或搜刮的片段。

    回傳格式 (JSON Only)：
    [
      {"start": 12.5, "end": 18.0, "reason": "視覺偵測：畫面中央跳出紅色碎甲數字，隨後右上角顯示擊倒通知"},
      {"start": 45.0, "end": 50.0, "reason": "視覺偵測：玩家使用鳳凰治療包，且護甲條正在回復"}
    ]
    """

    # 4. 調整參數：讓它嚴謹一點 (Temperature 0.1)
    try:
        response = model.generate_content(
            [video_file, prompt],
            generation_config={
                "response_mime_type": "application/json",
                "temperature": 0.1,  # 降低隨機性，不讓 AI 瞎掰
                "top_p": 0.95
            }
        )

        # 顯示並儲存結果
        print("-" * 30)
        print("📋 分析結果：")
        print(response.text)

        # 自動存檔到 out 資料夾
        out_path = os.path.join("out", f"{video_name}_vision_pro.json")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"\n💾 詳細報告已儲存：{out_path}")

    except Exception as e:
        print(f"\n❌ 分析過程發生錯誤：{e}")


if __name__ == "__main__":
    # 自動抓 data/in 裡面的影片來跑
    video_dir = os.path.join("data", "in")

    if not os.path.exists(video_dir):
        print(f"❌ 找不到資料夾：{video_dir}")
        exit(1)

    files = [f for f in os.listdir(
        video_dir) if f.lower().endswith((".mp4", ".mkv", ".mov"))]

    if files:
        for f in files:
            analyze_video_with_gemini(os.path.join(video_dir, f))
    else:
        print("❌ data/in 資料夾裡面沒有影片！請放一個 .mp4 進去測試。")
