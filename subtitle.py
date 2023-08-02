from manim import *
from datetime import datetime

def parse_subtitle(filename):
  file1 = open(filename, 'r')
  Lines = list(filter(lambda line: len(line.strip()) > 0, file1.readlines()))
  fmt = '%M:%S.%f'
  diffs = filter(lambda line: len(line.strip().split('-->')) > 1, Lines)
  texts = list(filter(lambda line: len(line.strip().split('-->')) == 1, Lines))
  texts = list(map(lambda str: str.strip(), texts))
  diffs = list(diffs)
  res = []
  for diff in diffs:
    dates = list(map(lambda str: datetime.strptime(str.strip(), fmt), diff.strip().split('-->')))
    res.append((dates[1] - dates[0]).seconds)

  return list(zip(texts, res))

class IterateColor(Scene):
    def construct(self):
      lines = parse_subtitle('01 - Bela Kiss.vtt')
      for (text, duration) in lines:
         self.animate_line(text, duration)

    def animate_line(self, text, duration):
        text1_mob = Text(text, font_size=24)
        self.add(text1_mob)
        for word in text1_mob.split():
          self.play(word.animate.set_color(RED), run_time=duration/len(text1_mob.split()))
        self.remove(text1_mob)
