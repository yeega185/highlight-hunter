try:
    from moviepy import VideoFileClip
    print("✅ MoviePy 成功讀取！工具準備好了。")
except ImportError:
    print("❌ 還是找不到 MoviePy，請確認第一步是否有報錯。")
