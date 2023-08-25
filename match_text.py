import json
from functools import reduce
 
def parse_segments(filename):
  f = open(filename)
  data = json.load(f)

  words = []
  for segment in data['segments']:
    words = words + segment['words']

  return words

# Opening JSON file

# print(parse_segments('transcript.json'))

def parse_lyrics(filename):
  text_file = open(filename, "r")

  #read whole file to a string
  data = text_file.read()

  #close file
  text_file.close()
  words = list(reduce(lambda a,b: a + b, map(lambda line: line.split(' '), data.split('\n'))))
  return words
  
def match_text(transcript, actual_lyrics):
  words_timed = parse_segments(transcript)
  len_timed = len(words_timed)
  words = parse_lyrics(actual_lyrics)
  len_words = len(words)

  result = []
  words_i = 0

  for i, word_timed in enumerate(words_timed):
    timed = word_timed['word']
    start = word_timed['start']
    end = word_timed['end']
    actual_text = words[word_i]
    ratio = len(timed) / len(actual_text)
    if ratio > 1.5:
      while ratio > 1.5:
        word_i += 1
        actual_text += words[word_i]
        ratio = len(timed) / len(actual_text)
    if ratio < 0.66:
      while ratio < 0.66:
        timed += words_timed[i+1]['word']
        ratio = len(timed) / len(actual_text)
    
    result.append({
      start: word['start']
      end: word['end']
      word: actual_text
    })

  print(result)


    

# parse_lyrics('lyrics.txt')
match_text('transcript.json', 'lyrics.txt')