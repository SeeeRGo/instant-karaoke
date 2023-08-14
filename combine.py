import ffmpeg

input = ffmpeg.input('./media/videos/1080p60/IterateColor.mp4').video
audio = ffmpeg.input('./output/Kitty In A Casket - Cold Black Heart/accompaniment.wav').audio
out = ffmpeg.output(audio, input, 'out.mp4').run()
