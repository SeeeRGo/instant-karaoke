import whisper
from manim import *
from spleeter.separator import Separator
import ffmpeg

def separate_file(filename):
  separator = Separator('spleeter:2stems')

  separator.separate_to_file(filename, '/output/')

def transcribe_file(filename):
  model = whisper.load_model("base.en")
  result = model.transcribe(filename, word_timestamps=True)
  return result['segments']

  # print(segments)
  # for segment in segments:
  #   words = segment['words']
  #   print('text: ', segment['text'])
  #   for word in words:
  #       print('word: ', word['word'], 'start: ', word['start'], 'end: ', word['end'])



class IterateColor(Scene):
    def construct(self):
      segments = transcribe_file("Kitty In A Casket - Cold Black Heart.mp3")
      # transcribe_file("Kitty In A Casket - Cold Black Heart.mp3")


      # for (text, duration) in lines:
      #    self.animate_line(text, duration)
      for segment in segments:
        words = segment['words']
        # print('text: ', segment['text'])
        # print('words: ', segment['words'])
        # text1_mob = Text(segment['text'], font_size=24)
        # self.add(text1_mob)
        texts = []
        for word in words:
          # print('word: ', word['word'], 'start: ', word['start'], 'end: ', word['end'])
          
          texts.append((Text(word['word'], font_size=24), word['end'] - word['start']))

        # print(texts)
        for (word, duration) in texts:
          self.add(word)
          self.play(word.animate.set_color(RED), run_time=duration)
          self.remove(word)
          
        # for (word, duration) in texts:

        # for (word) in texts:
    def animate_line(self, text, duration):
        text1_mob = Text(text, font_size=24)
        self.add(text1_mob)
        for word in text1_mob.split():
          self.play(word.animate.set_color(RED), run_time=duration/len(text1_mob.split()))
        self.remove(text1_mob)

# with tempconfig({"quality": "medium_quality", "preview": True}):
scene = IterateColor()
scene.render()

input = ffmpeg.input('./media/videos/1080p60/IterateColor.mp4')
audio = ffmpeg.input('/output/Kitty In A Casket - Cold Black Heart/accompaniment.wav')
# audio = ffmpeg.input('Kitty In A Casket - Cold Black Heart.mp3')
# video = input.video.hflip()
out = ffmpeg.output(audio, input, 'out.mp4', codec='copy').run()
#   print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
# for segment in segments:
#     print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))

# from faster_whisper import WhisperModel

# model_size = "base"

# # Run on GPU with FP16
# model = WhisperModel(model_size, device="auto", compute_type="int8")

# # or run on GPU with INT8
# # model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
# # or run on CPU with INT8
# # model = WhisperModel(model_size, device="cpu", compute_type="int8")

# segments = model.transcribe("01 - Bela Kiss.mp3", beam_size=5, language="English")

# # print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

# for segment in segments:
#     print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))