import whisper
import json
import os

# --- 設定區：這裏改一次就好，不用去下面翻程式碼 ---
TARGET_MODEL = "medium"  # 如果顯存夠可以改 "medium"
GAME_TYPE = "Apex Legends"
APEX_state = "臉上,  拉大電, 拉小電, 拉鳳凰, 黃, 黃雀, 倒地,換甲,補電, 拉補 "
APEX_supply = "破甲, 紅甲, 金甲, 白甲, 藍甲, 紫甲, 金包 "
APEX_Role = "惡靈, 腐蝕, 亡靈, 尋血犬, 暗碼士, 羅巴, 狗,"
Apex_weapon = "Car, 克萊柏, R99, R301, 伏特, 電槍, 電磁槍, 霰彈, 狙擊, 長槍, LMG, 機槍 "
APEX_Skill = "大招, 拉洞, 縮圈, EMP, 小飛機"
# ----------------------------------------------


def run_transcription(file_path, output_json):
    """核心轉錄邏輯"""
    print(f"\n[highlight-hunter] 啟動辨識：{os.path.basename(file_path)}")

    # 1. 載入模型
    model = whisper.load_model(TARGET_MODEL)

    # 2. 設定提示詞 (只給關鍵字，不給指令，避免 AI 產生幻覺重複指令)
    prompt_context = f" 這是，{GAME_TYPE} 遊戲對話影片，{APEX_Role} {Apex_weapon} {APEX_state} {APEX_supply} {APEX_Skill} 。"

    # 3. 執行辨識 (加入穩定性參數)
    # condition_on_previous_text=False 是防止「重複跳針」的最重要設定
    result = model.transcribe(
        file_path,
        initial_prompt=prompt_context,
        condition_on_previous_text=False,
        # --- 新增/調整以下參數 ---
        # 降低隨機性，讓輸出更穩定（0.0 到 1.0，越低越嚴謹）
        temperature=0.2,
        no_speech_threshold=0.6,
        fp16=False,
        # 增加搜尋寬度，讓 AI 多思考幾種可能性（預設 5
        beam_size=5
    )

    # 4. 封裝成 JSON
    output_data = {
        "project": "highlight-hunter",
        "file_name": os.path.basename(file_path),
        "transcript": [
            {
                "start": round(seg['start'], 2),
                "end": round(seg['end'], 2),
                "text": seg['text'].strip()
            } for seg in result['segments']
        ]
    }

    # 5. 存檔
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=4, ensure_ascii=False)
    print(f"✅ 產出成功：{output_json}")


if __name__ == "__main__":
    # 自動偵測路徑
    in_dir = os.path.join("data", "in")
    out_dir = "out"

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    # 抓取所有影片格式
    video_list = [f for f in os.listdir(
        in_dir) if f.lower().endswith(('.mp4', '.mkv', '.mov'))]

    if not video_list:
        print(f"❌ 錯誤：在 {in_dir} 資料夾內沒看到影片。")
    else:
        print(f"🚀 開始批次處理，共 {len(video_list)} 個檔案...")
        for video_name in video_list:
            full_input_path = os.path.join(in_dir, video_name)
            full_output_path = os.path.join(
                out_dir, f"{os.path.splitext(video_name)[0]}_transcript.json")

            try:
                run_transcription(full_input_path, full_output_path)
            except Exception as e:
                print(f"💥 處理 {video_name} 失敗：{e}")
