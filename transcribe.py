import whisper
from manim import *
from spleeter.separator import Separator
from spleeter.audio.adapter import AudioAdapter
from match_text import match_text
import os
from supabase import create_client, Client
from dotenv import load_dotenv

def separate_file(filename, output_path):
  separator = Separator('spleeter:2stems')

  audio_loader = AudioAdapter.default()
  sample_rate = 44100
  waveform, _ = audio_loader.load(filename, sample_rate=sample_rate)

  prediction = separator.separate(waveform)
  audio_loader.save(output_path, prediction['accompaniment'], sample_rate=sample_rate)

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
    def __init__(self, filename, **kwargs):
      self.filename = filename
      return Scene.__init__(self, **kwargs)

    def construct(self):
      last_end = 0
      output_path = './output/accompaniment.wav'
      separate_file(self.filename, './output/accompaniment.wav')
      segments = transcribe_file(self.filename)
      segments = match_text(segments, 'actual_lyrics.txt')
      self.add_sound(output_path)
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

if __name__ == "__main__":
  load_dotenv()
  scene = IterateColor("01 - Bela Kiss.mp3")
  scene.render()
  url: str = os.environ.get("SUPABASE_URL")
  key: str = os.environ.get("SUPABASE_KEY")
  print(key)
  supabase: Client = create_client(url, key)
  file = open('./media/videos/1080p60/IterateColor.mp4','rb')
  res = supabase.storage.from_('file_queue').upload("01 - Bela Kiss.mp4", file)
  
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