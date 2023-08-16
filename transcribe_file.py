import whisper

def transcribe_file(filename):
  model = whisper.load_model("large-v2")
  result = model.transcribe(filename, word_timestamps=True)
  f = open("transcript_splited.txt", "a")
  f.write(str(result))
  f.close()
  return result['segments']

segments = transcribe_file("./output/Kitty In A Casket - Cold Black Heart/vocals.wav")
# # print(segments)

# for segment in segments:
#   words = segment['words']
#   print('text: ', segment['text'])
#   for word in words:
#       print('word: ', word['word'], 'start: ', word['start'], 'end: ', word['end'])
