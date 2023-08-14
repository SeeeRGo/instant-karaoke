import whisper
from manim import *

def transcribe_file(filename):
  model = whisper.load_model("base.en")
  result = model.transcribe(filename, word_timestamps=True)
  return result['segments']

class IterateColor(Scene):
    def construct(self):
      segments = transcribe_file("Kitty In A Casket - Cold Black Heart.mp3")
      last_end = 0
      for segment in segments:
        words = segment['words']
        texts = []
        for word in words:
          # print('word: ', word['word'], 'start: ', word['start'], 'end: ', word['end'])
          
          texts.append((Text(word['word'], font_size=24), word['end'] - word['start'], word['start'] - last_end))
          last_end = word['end']

        # print(texts)
        for (word, duration, wait) in texts:
          print('duration:', duration, 'wait: ', wait)
          self.add(word)
          # if wait > 0:
          #   self.wait(wait)
          self.play(word.animate.set_color(RED), run_time=duration)
          self.remove(word)

scene = IterateColor()
scene.render()
