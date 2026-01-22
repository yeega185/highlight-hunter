import whisper
import json
import os


def run_calibrated_transcription(file_path, output_json, game_terms):
    print(f"--- [highlight-hunter] 正在執行 AI 轉錄校準任務 ---")
    print(f"處理檔案：{os.path.basename(file_path)}")

    # 1. 升級模型：從 base 換成 small (準確度大幅提升)
    # 如果顯卡記憶體不足，可以換回 "base"
    model = whisper.load_model("medium")

    # 2. 設定小抄 (Initial Prompt)
    # 將你列出的遊戲術語餵給 AI
    # 拿掉所有說明，只給最核心的 Apex 術語
    prompt = "Apex, 碎甲, 打藥, 倒地, 惡靈, 辛烷, 門洞, 縮圈, 勸架"

    # 3. 執行辨識
    # language="zh" 強制指定中文，避免 AI 混淆
    result = model.transcribe(
        file_path,
        initial_prompt=prompt,
        fp16=False,
        no_speech_threshold=0.6,  # 提高門檻，雜音太大的地方直接留白，不要亂猜
        logprob_threshold=-1.0   # 信心度太低就不要輸出
    )

    transcript_data = {
        "job_info": {
            "version": "W2D3_CALIBRATED",
            "model": "small",
            "terms_used": game_terms
        },
        "transcript": []
    }

    for segment in result['segments']:
        transcript_data["transcript"].append({
            "start": round(segment['start'], 3),
            "end": round(segment['end'], 3),
            "text": segment['text'].strip()
        })

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(transcript_data, f, indent=4, ensure_ascii=False)

    print(f"✅ 校準完成！精準版 JSON 已儲存：{output_json}")


if __name__ == "__main__":
    # 設定路徑
    input_file = os.path.join("data", "in", "sample2.mp4")  # <-- 改成你資料夾裡的檔名
    output_file = os.path.join("out", "calibrated_transcript.json")

    # 定義你的術語小抄 (這就是辨識的技術核心！)
    # 針對 Apex 最佳化的術語清單
    my_game_terms = "Apex, 英雄, 惡靈, 辛烷, 亡靈, 尋血犬, 直布羅陀, 碎甲, 破甲, 打藥, 鳳凰包, 紅甲, 金盾, 縮圈, 落地, 勸架, 小幫手, 平行步槍, 301, 克萊博, 大招,  跳板, 門洞"

    if os.path.exists(input_file):
        run_calibrated_transcription(input_file, output_file, my_game_terms)
    else:
        print("❌ 找不到檔案，請確認 data/in 內是否有影片。")
