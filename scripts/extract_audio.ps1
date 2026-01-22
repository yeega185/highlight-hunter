param(
  # 只參數化「輸入」：執行時可用 -InputFile 指定影片
  [string]$InputFile = "data/in/sample.mp4"
)

# 輸出固定（符合 W1 規格：固定命名 audio.wav）
$OutputFile = "out/audio.wav"

# 檢查輸入檔是否存在
if (-not (Test-Path $InputFile)) {
  Write-Host "Input not found: $InputFile"
  exit 1
}

# 確保 out/ 資料夾存在
if (-not (Test-Path "out")) {
  New-Item -ItemType Directory -Path "out" | Out-Null
}

# 抽音訊：WAV / 16kHz / mono
ffmpeg -y -i $InputFile -vn -ac 1 -ar 16000 -c:a pcm_s16le $OutputFile

Write-Host "Done: $OutputFile"
