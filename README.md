# highlight-hunter (W1)

## Day 1 — Project setup

**Goal:** Create a reproducible project structure and fix the Week 1 I/O spec.

### Project structure

* `data/in/` : input video (local only)
* `out/` : outputs (local only)
* `scripts/` : runnable scripts

### Week 1 fixed spec

* Input: `data/in/sample.mp4`
* Output: `out/audio.wav`
* Audio spec: WAV, 16kHz, mono
* Naming: output fixed as `audio.wav` for Week 1

### .gitignore (required)

Create `.gitignore` in project root to avoid uploading large files:

```gitignore
data/in/
out/
*.wav
*.mp4
```

---

## Day 2 — Extract audio (manual command)

**Goal:** Export `out/audio.wav` from `data/in/sample.mp4`.

Run in PowerShell at project root:

```powershell
cd "D:\Portfolio\highlight-hunter"
ffmpeg -y -i "data/in/sample.mp4" -vn -ac 1 -ar 16000 -c:a pcm_s16le "out/audio.wav"
```

Verify:

```powershell
ffmpeg -i "out/audio.wav"
```

Expected: `16000 Hz, mono`

---

## Day 3 — Extract audio (script)

**Goal:** Make Day 2 reproducible with one command.

Run:

```powershell
powershell -ExecutionPolicy Bypass -File "scripts/extract_audio.ps1"
```

Script file:

* `scripts/extract_audio.ps1`

Script content:

```powershell
# extract_audio.ps1
# Convert data/in/sample.mp4 -> out/audio.wav (16kHz mono)

$inputPath  = "data/in/sample.mp4"
$outputPath = "out/audio.wav"

ffmpeg -y -i $inputPath -vn -ac 1 -ar 16000 -c:a pcm_s16le $outputPath

Write-Host "Done: $outputPath"
```

## Day 5 — README 補充：如何產出 audio.wav（固定命名）

### 目標
- 固定輸出：`out/audio.wav`
- 音訊規格：WAV / 16kHz / mono

### 方法 A：用腳本（推薦）
在專案根目錄執行：
```powershell
powershell -ExecutionPolicy Bypass -File "scripts/extract_audio.ps1"
```

## Day 6 — Script update：Input 參數化（Output 固定）

### 目標
- 讓 `scripts/extract_audio.ps1` 支援 `-InputFile`
- 輸出仍固定為 `out/audio.wav`（維持 W1 命名一致）

### 用法
使用預設輸入（`data/in/sample.mp4`）：
```powershell
powershell -ExecutionPolicy Bypass -File "scripts/extract_audio.ps1"
```
