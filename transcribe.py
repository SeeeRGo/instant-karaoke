import whisper
from manim import *
from spleeter.separator import Separator
from spleeter.audio.adapter import AudioAdapter
from match_text import match_text

def separate_file(filename, output_path, vocals_path):
  separator = Separator('spleeter:5stems')

  audio_loader = AudioAdapter.default()
  sample_rate = 44100
  waveform, _ = audio_loader.load(filename, sample_rate=sample_rate)

  prediction = separator.separate(waveform)
  audio_loader.save(output_path, prediction['other'], sample_rate=sample_rate)
  audio_loader.save(vocals_path, prediction['vocals'], sample_rate=sample_rate)

def transcribe_file(filename):
  model = whisper.load_model("large-v2")
  result = model.transcribe(filename, word_timestamps=True)
  return result['segments']

  # print(segments)
  # for segment in segments:
  #   words = segment['words']
  #   print('text: ', segment['text'])
  #   for word in words:
  #       print('word: ', word['word'], 'start: ', word['start'], 'end: ', word['end'])



class IterateColor(Scene):
    def __init__(self, filename, lyrics, output_path, vocals_path, **kwargs):
      self.filename = filename
      self.lyrics = lyrics
      self.output_path = output_path
      self.vocals_path = vocals_path
      self.timeline = []
      return Scene.__init__(self, **kwargs)

    def construct(self):
      last_end = 0
      separate_file(self.filename, self.output_path, self.vocals_path)
      segments = transcribe_file(self.vocals_path)
      segments = match_text(segments, self.lyrics)
      self.timeline = segments
      time = 0

      for i,segment in enumerate(segments):
        word_list_parsed = []
        word_list = segment['words']
        total = 0
        words = ''

        for w in word_list:
            wait_time = w['start'] - last_end
            last_end = w['end']
            word = w['word']
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
        