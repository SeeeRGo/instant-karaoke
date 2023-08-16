import whisper
from manim import *
# from spleeter.separator import Separator
# import ffmpeg
# from manim import config as global_config

# config = global_config.copy()
# config.disable_caching = True

# def separate_file(filename):
#   separator = Separator('spleeter:2stems')

#   separator.separate_to_file(filename, './output')

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
    def construct(self):
      filename = "Kitty In A Casket - Cold Black Heart.mp3"
      segments = transcribe_file(filename)      
      last_end = 0
      # separate_file(filename)
      self.add_sound('./output/Kitty In A Casket - Cold Black Heart/vocals.wav')
      for segment in segments:
        word_list_parsed = []
        word_list = segment['words']
        words = ''
        total = 0
        for w in word_list:
            wait_time = w['start'] - last_end
            last_end = w['end']
            word_list_parsed.append((w['end'] - w['start'], len(w['word'].replace(' ', '_')), wait_time))
            words += w['word'].replace(' ', '_')
            total += len(w['word'].replace(' ', '_'))
        text = segment['text'].replace(' ', '_')
        text1 = Text(text, font_size=24)
        print(len(text1), total)
        if total > len(text1):
          text1 = Text(f'{text}.', font_size=24)
        self.add(text1)
        offset = 0
        for (duration, length, wait) in word_list_parsed:
          if wait > 0:
            self.wait(wait)
          next_offset = offset + length
          for i in range(offset, next_offset):
            letter = text1[i]
            run_time = round(duration * 90/length) / 90
            self.play(letter.animate.set_color(RED), run_time=run_time)

          offset = next_offset

        self.remove(text1)


scene = IterateColor()
scene.render()

# input = ffmpeg.input('./media/videos/1080p60/IterateColor.mp4').video
# audio = ffmpeg.input('./output/Kitty In A Casket - Cold Black Heart/vocals.wav').audio
# out = ffmpeg.output(audio, input, 'out.mp4').run()

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