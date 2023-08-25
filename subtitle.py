import whisper
from manim import *

def transcribe_file(filename):
  model = whisper.load_model("tiny.en")
  result = model.transcribe(filename, word_timestamps=True)
  return result['segments']

class IterateColor(Scene):
    def __init__(self, filename, **kwargs):
      self.filename = filename
      return Scene.__init__(self, **kwargs)

    def construct(self):
      last_end = 0
      output_path = 'Kitty In A Casket - Cold Black Heart.mp3'
      # separate_file(self.filename, '/output/accompaniment.wav')
      segments = transcribe_file(self.filename)
      self.add_sound(output_path)
      time = 0
      file1 = open('lyrics.txt', 'r')
      Lines = file1.readlines()

      for i,segment in enumerate(segments):
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

        text = Lines[i].strip()
        text1 = Text(text, font_size=24)

        if total > len(text1):
          text1 = Text(text + '_', font_size=24)

        self.add(text1)
        offset = 0

        for (duration, length, wait) in word_list_parsed:
          if wait > 0:
            self.wait(round(wait * 60) /60)

          time += wait
          time += duration
          next_offset = offset + length

          if next_offset > len(text1):
            next_offset = len(text1)

          for i in range(offset, next_offset):
            letter = text1[i]
            run_time = round(duration * 60/length) / 60
            self.play(letter.animate.set_color(RED), run_time=run_time)

          offset = next_offset

        self.remove(text1)

scene = IterateColor(filename="Kitty In A Casket - Cold Black Heart.mp3")
scene.render()
