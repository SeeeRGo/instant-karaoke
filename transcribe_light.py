import whisper
from manim import *
from spleeter.separator import Separator
from spleeter.audio.adapter import AudioAdapter
from match_text import match_text, parse_segments
from dotenv import load_dotenv

def separate_file(filename, output_path):
  separator = Separator('spleeter:2stems')

  audio_loader = AudioAdapter.default()
  sample_rate = 44100
  waveform, _ = audio_loader.load(filename, sample_rate=sample_rate)

  prediction = separator.separate(waveform)
  audio_loader.save(output_path, prediction['vocals'], sample_rate=sample_rate)

def transcribe_file(filename):
  model = whisper.load_model("large-v2")
  result = model.transcribe(filename, word_timestamps=True)
  return result['segments']

import json

def parse_segments_from_file(filename):
  f = open(filename)
  data = json.load(f)

  return data['segments']



class IterateColorSeparated(Scene):
    def __init__(self, filename, **kwargs):
      self.filename = filename
      return Scene.__init__(self, **kwargs)

    def construct(self):
      last_end = 0
      output_path = './output/accompaniment.wav'
      separate_file(self.filename, './output/accompaniment.wav')
      # segments = parse_segments_from_file(output_path)
      segments = transcribe_file(output_path)
      segments = parse_segments(segments)
      segments = match_text(segments, 'actual_lyrics.txt')
      self.add_sound(self.filename)
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

        for (duration, length, wait) in word_list_parsed:
          if wait > 0:
            self.wait(round(wait * 60) /60)

          offset = 0
          next_offset = offset + length

          if next_offset > len(text1):
            next_offset = len(text1)
          time += wait
          time += duration
          # letters = text1[offset:next_offset]
          self.wait(round(duration * 60) / 60)
          # self.play(letters.animate.set_color(RED), run_time=round(duration * 60) / 60)
        self.remove(text1)

if __name__ == "__main__":
  load_dotenv()
  scene = IterateColorSeparated("01 - Bela Kiss.mp3")
  scene.render()
  # url: str = os.environ.get("SUPABASE_URL")
  # key: str = os.environ.get("SUPABASE_KEY")
  # print(key)
  # supabase: Client = create_client(url, key)
  # file = open('./media/videos/1080p60/IterateColor.mp4','rb')
  # res = supabase.storage.from_('file_queue').upload("01 - Bela Kiss.mp4", file)
