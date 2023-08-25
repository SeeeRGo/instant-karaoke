import whisper
from manim import *
from spleeter.separator import Separator
from spleeter.audio.adapter import AudioAdapter

def separate_file(filename, output_path):
  separator = Separator('spleeter:2stems')

  audio_loader = AudioAdapter.default()
  sample_rate = 44100
  waveform, _ = audio_loader.load(filename, sample_rate=sample_rate)

  prediction = separator.separate(waveform)
  audio_loader.save(output_path, prediction['vocals'], sample_rate=sample_rate)

def transcribe_file(filename):
  model = whisper.load_model("medium.en")
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
      output_path = '/output/accompaniment.wav'
      separate_file(self.filename, '/output/accompaniment.wav')
      segments = transcribe_file(self.filename)
      self.add_sound(output_path)
      time = 0
      file1 = open('/project/actual_lyrics.txt', 'r')
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
          text1 = Text(f'{text}_', font_size=24)

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