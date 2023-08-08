import whisper
from manim import *

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
      # for (text, duration) in lines:
      #    self.animate_line(text, duration)
      for segment in segments:
        words = segment['words']
        # print('text: ', segment['text'])
        # text1_mob = Text(segment['text'], font_size=24)
        # self.add(text1_mob)
        for word in words:
          # print('word: ', word['word'], 'start: ', word['start'], 'end: ', word['end'])
          text1_mob = Text(word['word'], font_size=24)
          self.add(text1_mob)   
          self.play(text1_mob.animate.set_color(RED), run_time=(word['end'] - word['start']))
          self.remove(text1_mob)
    def animate_line(self, text, duration):
        text1_mob = Text(text, font_size=24)
        self.add(text1_mob)
        for word in text1_mob.split():
          self.play(word.animate.set_color(RED), run_time=duration/len(text1_mob.split()))
        self.remove(text1_mob)

# with tempconfig({"quality": "medium_quality", "preview": True}):
scene = IterateColor()
scene.render()
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