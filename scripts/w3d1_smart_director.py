import json
import os

# 1. 設定
INPUT_JSON_DIR = "out"
OUTPUT_JSON_DIR = "out"


def refine_highlights(json_filename):
    input_path = os.path.join(INPUT_JSON_DIR, json_filename)
    output_path = os.path.join(OUTPUT_JSON_DIR, f"refined_{json_filename}")

    print(f"🧠 AI 導演正在審閱劇本：{json_filename}")

    with open(input_path, 'r', encoding='utf-8') as f:
        raw_events = json.load(f)

    refined_events = []

    # --- 第一階段：邏輯修剪 (Trimming Rules) ---
    print("✂️  正在執行：智慧縮減規則...")
    for event in raw_events:
        start = event['start']
        end = event['end']
        reason = event['reason']
        duration = end - start

        new_start = start
        new_end = end

        # 規則 A：補血類 (Healing) - 通常很長，我們只想要最後成功的瞬間
        # 關鍵字：治療包, 電池, 鳳凰
        if any(k in reason for k in ["治療包", "電池", "鳳凰", "補血"]):
            if duration > 8.0:  # 如果補血動作超過 8 秒
                print(f"   - 發現冗長補血 ({duration:.1f}s)，只保留最後 6 秒...")
                new_start = end - 6.0
                event['reason'] = f"{reason} (AI精修: 保留最後6秒)"

        # 規則 B：擊殺類 (Kill/Damage) - 這是重點，稍微往前多抓一點緩衝
        elif any(k in reason for k in ["擊倒", "擊殺", "傷害", "破甲"]):
            new_start = max(0, start - 2.0)  # 往前多抓 2 秒鋪陳
            new_end = end + 1.0  # 往後多抓 1 秒確認
            event['reason'] = f"{reason} (AI精修: 增加戰鬥緩衝)"

        # 儲存修剪後的結果
        refined_events.append({
            "start": round(new_start, 2),
            "end": round(new_end, 2),
            "reason": event['reason']
        })

    # --- 第二階段：合併重疊 (Merge Overlaps) ---
    # 如果片段 A 是 10~15秒，片段 B 是 14~20秒，應該合併成 10~20秒，而不是剪兩次
    print("🔗 正在執行：時間軸合併...")
    if not refined_events:
        print("❌ 沒有片段可以處理")
        return

    # 先依開始時間排序
    refined_events.sort(key=lambda x: x['start'])

    final_events = []
    current_evt = refined_events[0]

    for next_evt in refined_events[1:]:
        # 如果 下一個片段的開始時間 < 當前片段的結束時間 + 2秒緩衝
        if next_evt['start'] <= current_evt['end'] + 2.0:
            # 合併！結束時間取兩者最晚的
            current_evt['end'] = max(current_evt['end'], next_evt['end'])
            # 把理由接在一起
            if next_evt['reason'] not in current_evt['reason']:
                current_evt['reason'] += " + " + next_evt['reason']
            print(
                f"   - 合併相鄰事件 -> {current_evt['start']}s 至 {current_evt['end']}s")
        else:
            # 沒有重疊，儲存當前片段，切換到下一個
            final_events.append(current_evt)
            current_evt = next_evt

    # 別忘了最後一個
    final_events.append(current_evt)

    # --- 輸出結果 ---
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(final_events, f, indent=2, ensure_ascii=False)

    print("-" * 30)
    print(f"✅ 劇本優化完成！")
    print(f"   原始片段數：{len(raw_events)}")
    print(f"   精修片段數：{len(final_events)}")
    print(f"   輸出檔案：{output_path}")


if __name__ == "__main__":
    # 這裡填入你剛剛 W2 產出的那個 JSON 檔名
    TARGET_JSON = "sample2.mp4_vision_pro.json"

    if os.path.exists(os.path.join(INPUT_JSON_DIR, TARGET_JSON)):
        refine_highlights(TARGET_JSON)
    else:
        print("❌ 找不到 JSON 檔案")
