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

print(parse_segments('transcript.json'))

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

  print('timed', len_timed, 'words', len_words)

  # for i,word_timed in enumerate(words_timed):
    

# parse_lyrics('lyrics.txt')