import whisper

def transcribe_file(filename):
  model = whisper.load_model("base.en")
  result = model.transcribe(filename, word_timestamps=True)
  return result['segments']

segments = transcribe_file("Kitty In A Casket - Cold Black Heart.mp3")
# print(segments)

for segment in segments:
  words = segment['words']
  print('text: ', segment['text'])
  for word in words:
      print('word: ', word['word'], 'start: ', word['start'], 'end: ', word['end'])
