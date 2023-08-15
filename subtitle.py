import whisper
from manim import *

def transcribe_file(filename):
  model = whisper.load_model("tiny.en")
  result = model.transcribe(filename, word_timestamps=True)
  return result['segments']

class IterateColor(Scene):
    def construct(self):
      segments = transcribe_file("Kitty In A Casket - Cold Black Heart.mp3")
      last_end = 0
      for segment in segments:
        # self.add(text1)
        word_list_parsed = []
        word_list = segment['words']
        words = ''
        total = 0
        for w in word_list:
            wait_time = w['start'] - last_end
            last_end = w['end']
            word_list_parsed.append((w['end'] - w['start'], len(w['word'].strip()), wait_time))
            words += w['word'].strip()
            total += len(w['word'].strip())

        text1 = Text(segment['text'], font_size=24)
        self.add(text1)

        offset = 0
        for (duration, length, wait) in word_list_parsed:
          if wait > 0:
            self.wait(wait)
          next_offset = offset + length
          if offset + length > len(text1):
            next_offset = len(text1)
          for i in range(offset, next_offset):
            print('offset: ', offset, 'offset + length: ', offset + length, 'i: ', i)
            letter = text1[i]
            self.play(letter.animate.set_color(RED), run_time=duration/length)

          offset = next_offset

        self.remove(text1)

scene = IterateColor()
scene.render()
