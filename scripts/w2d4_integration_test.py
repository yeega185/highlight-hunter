import json
import os
from moviepy import VideoFileClip, concatenate_videoclips

# 1. 設定檔案路徑
VIDEO_DIR = "data/in"
JSON_DIR = "out"
OUTPUT_DIR = "data/highlights"

# 確保輸出資料夾存在
os.makedirs(OUTPUT_DIR, exist_ok=True)


def create_highlight_video(video_filename, json_filename):
    video_path = os.path.join(VIDEO_DIR, video_filename)
    json_path = os.path.join(JSON_DIR, json_filename)
    output_path = os.path.join(OUTPUT_DIR, f"highlight_{video_filename}")

    print(f"🎬 開始製作精華影片：{video_filename}")

    # 讀取 JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        highlights = json.load(f)

    # 載入原始影片
    try:
        original_clip = VideoFileClip(video_path)
    except Exception as e:
        print(f"❌ 無法讀取影片 {video_path}: {e}")
        return

    clips = []
    print(f"🔍 找到 {len(highlights)} 個精彩片段，開始剪輯...")

    for i, h in enumerate(highlights):
        start = h['start']
        end = h['end']
        reason = h['reason']

        # 安全檢查：避免結束時間超過影片長度
        if end > original_clip.duration:
            end = original_clip.duration
        if start >= end:
            continue

        print(f"  ✂️ cutting clip {i+1}: {start}s - {end}s ({reason})")

        # 剪切片段
        clip = original_clip.subclipped(start, end)
        clips.append(clip)

    if clips:
        # 合併所有片段
        print("🔗 正在合併所有片段...")
        final_clip = concatenate_videoclips(clips)

        # 輸出檔案
        final_clip.write_videofile(
            output_path, codec="libx264", audio_codec="aac")
        print(f"✅ 精華影片已完成！儲存於：{output_path}")
    else:
        print("⚠️ JSON 裡沒有合法的剪輯區間，略過。")

    # 釋放資源
    original_clip.close()


if __name__ == "__main__":
    # 自動尋找配對的 JSON 和影片
    # 假設你的影片叫 sample2.mp4，JSON 叫 sample2.mp4_vision_pro.json

    # 這裡請填入你剛剛跑完的那個影片檔名
    TARGET_VIDEO = "sample2.mp4"
    TARGET_JSON = f"{TARGET_VIDEO}_vision_pro.json"

    if os.path.exists(os.path.join(JSON_DIR, TARGET_JSON)):
        create_highlight_video(TARGET_VIDEO, TARGET_JSON)
    else:
        print(f"❌ 找不到對應的 JSON 檔案：{TARGET_JSON}")
        print("請確認你已經跑完 test_gemini_vision.py 並且 out 資料夾裡有檔案。")
