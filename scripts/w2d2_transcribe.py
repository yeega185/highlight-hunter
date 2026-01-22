import whisper
import json
import os


def run_transcription(file_path, output_json):
    print(f"--- 開始處理：{os.path.basename(file_path)} ---")
    model = whisper.load_model("small")
    # Whisper 其實非常強大，它會自動呼叫 FFmpeg 處理各種影音格式
    result = model.transcribe(file_path, fp16=False)

    transcript_data = {
        "job_info": {
            "source_file": os.path.basename(file_path),
            "status": "TRANSCRIPT_DONE"
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

    print(f"✅ 成功產出：{output_json}\n")


if __name__ == "__main__":
    input_folder = os.path.join("data", "in")
    output_folder = "out"

    # 1. 定義你想支援的影片副檔名
    valid_extensions = ('.mp4', '.mkv', '.mov', '.avi', '.flv', '.wmv')

    # 2. 遍歷資料夾內所有檔案
    if not os.path.exists(input_folder):
        print(f"❌ 找不到資料夾：{input_folder}")
    else:
        # 找出符合副檔名的所有檔案
        all_files = [f for f in os.listdir(
            input_folder) if f.lower().endswith(valid_extensions)]

        if not all_files:
            print(f"🔍 在 {input_folder} 中沒看到任何影片檔案。")
        else:
            print(f"🚀 偵測到 {len(all_files)} 個檔案，準備開始全自動轉錄...")

            for file_name in all_files:
                input_path = os.path.join(input_folder, file_name)

                # 取得不含副檔名的主檔名
                base_name = os.path.splitext(file_name)[0]
                output_path = os.path.join(
                    output_folder, f"transcript_{base_name}.json")

                run_transcription(input_path, output_path)
