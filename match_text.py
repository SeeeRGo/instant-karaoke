import json
from functools import reduce
from jellyfish import soundex, match_rating_codex, nysiis, jaro_winkler_similarity, jaro_similarity, damerau_levenshtein_distance
import replace_words
 
def parse_segments(filename):
  f = open(filename)
  data = json.load(f)

  words = []
  for segment in data['segments']:
    words.append({
      "text": segment['text'],
      "words": [{
        "code": nysiis(word["word"].strip()),
        "word": word["word"].strip(),
        "start": word["start"],
        "end": word["end"]
        } for word in segment['words']]
    })

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
  return [{"code": nysiis(word), "word": word} for word in words]
  
def match_text(transcript, actual_lyrics):
  words_timed = parse_segments(transcript)
  words = parse_lyrics(actual_lyrics)

  remaining_words = words
  for segment in words_timed:
    text = segment['text']
    segment_codes = ' '.join([word["code"] for word in segment["words"]])
    stop = False
    best_match = 0
    text_match = 0
    actual_segment = ''
    actual_segment_codes = ''
    distance = 1000
    while(stop != True):
      for i,word in enumerate(remaining_words):
        new_match_score = jaro_similarity(segment_codes, actual_segment_codes + word['code'])
        text_match_score = jaro_similarity(text, actual_segment + word['word'])
        new_distance = damerau_levenshtein_distance(segment_codes, actual_segment_codes + word['code'])

        len_compare_continue = len(text) / len(actual_segment + word['word']) > 1.3
        text_compare = text_match_score > text_match and new_distance < distance

        if new_match_score > best_match or text_compare or len_compare_continue:
          best_match = new_match_score
          text_match = text_match_score
          distance = new_distance
          actual_segment_codes += word['code']
          actual_segment += word['word']
          actual_segment_codes += ' '
          actual_segment += ' '
        else:
          stop = True
          remaining_words = remaining_words[i:]
          break
    # break
    print(replace_words.replace_words(actual_segment.strip(), nums=segment['words']))



def getSoundexList(dList):
    res = [soundex(x) for x in dList]   # iterate over each elem in the dataList
    # print(res)     # ['T000', 'F630', 'F630', 'D263', 'T000', 'D263']
    return res

# print([x for x in sorted(getSoundexList(parse_segments('transcript.json')))])

match_text('transcript.json', 'lyrics.txt')
# print(parse_lyrics('lyrics.txt'))
# print(jaro_winkler_similarity('Staring on, perfection of love', 'Stared at in awe Perfection, no flaw'))
# print(jaro_winkler_similarity('Staring on, perfection of love', 'Stared at in awe Perfection, no flaw'))
