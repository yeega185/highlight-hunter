import json
import os
# 修改這行：適應新版 MoviePy
from moviepy import VideoFileClip


def run_integration_test():
    print("--- [highlight-hunter] W2D4: 整合測試啟動 ---")

    # 1. 設定路徑
    json_dir = "out"
    video_dir = os.path.join("data", "in")
    output_dir = os.path.join("data", "highlights")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 2. 定義我們要抓取的「精華關鍵字」
    # 你可以根據昨天 transcript.json 裡出現過的詞來改
    # 篩選清單 (對齊你 W2D3 設定的 APEX 術語)
    target_keywords = ["破甲", "倒", "紅甲", "換甲", "跟我一起", "孤郎", "鎖", "拉大電"]

    # 3. 掃描 JSON 檔案
    json_files = [f for f in os.listdir(
        json_dir) if f.endswith("_transcript.json")]

    for json_name in json_files:
        json_path = os.path.join(json_dir, json_name)
        # 對應影片檔名 (假設 JSON 名稱是 video_transcript.json)
        video_name = json_name.replace("_transcript.json", ".mp4")
        video_path = os.path.join(video_dir, video_name)

        if not os.path.exists(video_path):
            print(f"⚠️ 找不到對應影片：{video_name}，跳過。")
            continue

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # 注意：你的 JSON 結構是在 'transcript' 鍵值下
            segments = data.get("transcript", [])

        # 4. 尋找關鍵字並剪輯
        print(f"🔍 正在篩選：{video_name}")

        # 載入影片 (放在迴圈外減少消耗)
        # --- [邏輯核心] 加入旗標來檢查有無符合項目 ---
        has_match = False
        video = VideoFileClip(video_path)

        for i, seg in enumerate(segments):
            text = seg['text']
            # 檢查這段話有沒有我們要的關鍵字
            if any(key in text for key in target_keywords):
                has_match = True  # 找到符合項目，設定旗標為 True

                # 計算剪輯時間點
                start_t = max(0, seg['start'] - 5)   # 往前抓 5 秒，避免太突兀
                end_t = min(video.duration, seg['end'] + 25)  # 往後抓 25 秒
                print(f"✨ 發現精華！「{text}」於 {start_t}s，準備剪輯...")

                # 執行剪下
                highlight = video.subclipped(start_t, end_t)
                save_path = os.path.join(
                    output_dir, f"highlight_{i}_{video_name}")

                # 存檔 (使用快速編碼設定)
                highlight.write_videofile(
                    save_path, codec="libx264", audio_codec="aac")

        # --- [你要求的 Else 邏輯] ---
        if not has_match:
            print(f"ℹ️  結果：此檔案 ({video_name}) 中沒有符合的詞彙，不進行剪輯。")

        video.close()


if __name__ == "__main__":
    run_integration_test()
