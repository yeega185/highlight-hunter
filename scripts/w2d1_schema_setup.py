import json
import os

# 1. 定義你的輸出路徑 (依照行程表建議放在 out/ 資料夾)
output_dir = "out"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 2. 定義規格 (Schema)
# 這就是你跟未來的自己約定好的「合約」
# (1)job_info：這是為了對齊你文件中的「可追蹤性」 。如果以後你有 100 支影片，你才知道這份 JSON 是哪支影片產出的。
# (2)start / end 使用秒數 (Float)：這是為了對齊第 4 週的剪輯任務。FFmpeg 這類工具最喜歡這種格式（例如 12.5 秒），精確度高且好運算。
# (3)text：這是給第 3 週的 GPT 讀的，它會根據這段文字判斷「這是不是你要的高光」 。
# (4)維持使用「秒（帶小數點）」作為你的 JSON 規格。

schema_sample = {
    "job_info": {
        "job_id": "W2D1_INIT_TEST",
        "video_source": "pending",
        "format_version": "1.0"
    },
    "transcript": [
        {
            "start": 0.0,
            "end": 0.0,
            "text": "這裡是預留位置，明天 Whisper 會來填空"
        }
    ]
}

# 3. 產出規格檔案
file_path = os.path.join(output_dir, "transcript.json")
with open(file_path, "w", encoding="utf-8") as f:
    json.dump(schema_sample, f, indent=4, ensure_ascii=False)

print(f"✅ 第二週第一天任務完成！")
print(f"📁 規格檔案已建立於：{file_path}")
print(f"📝 明天的 Whisper 任務將會依照此格式寫入資料。")
