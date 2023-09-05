from manim import *

class AnimateTimeline(Scene):
    def __init__(self, segments, **kwargs):
      self.timeline = segments
      return Scene.__init__(self, **kwargs)

    def construct(self):
      last_end = 0
      time = 0

      for i,segment in enumerate(self.timeline):
        word_list_parsed = []
        word_list = segment['words']
        total = 0
        words = ''

        for w in word_list:
            wait_time = w['start'] - last_end
            last_end = w['end']
            word = w['text']
            word_list_parsed.append((w['end'] - w['start'], len(word), wait_time))
            words += f'{word} '
            total += len(word)

        text1 = Text(words.strip(), font_size=24)

        if total > len(text1):
          text1 = Text(f'{words.strip()}_', font_size=24)

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