import json
from functools import reduce
from jellyfish import soundex, match_rating_codex, nysiis, jaro_winkler_similarity, jaro_similarity, damerau_levenshtein_distance
import replace_words
 
def parse_segments(segments):

  words = []
  for segment in segments:
    words.append({
      "text": segment['text'],
      "start": segment['start'],
      "end": segment['end'],
      "words": [{
        "code": soundex(word["word"].strip()),
        "word": word["word"].strip(),
        "start": word["start"],
        "end": word["end"]
        } for word in segment['words']]
    })

  return words

# Opening JSON file

# print(parse_segments('transcript.json'))

def parse_lyrics(data):
  words = data.split('\n')
  res = []
  for line in words:
    for i,word in enumerate(line.split(' ')):
      res.append({"code": soundex(word), "word": word, "newline": i == 0})
  return res
  
def match_text(transcript, actual_lyrics):
  words_timed = parse_segments(transcript)
  words = parse_lyrics(actual_lyrics)

  remaining_words = words
  result = []
  for segment in words_timed:
    text = segment['text']
    segment_codes = ' '.join([word["code"] for word in segment["words"]])
    best_match = 0
    text_match = 0
    actual_segment = ''
    actual_segment_codes = ''
    num_lines = 0
    fill_lines = False
    for i,word in enumerate(remaining_words):
      if len(word["word"]) > 0:
        is_new_line = word['newline']
        new_match_score = jaro_similarity(segment_codes, actual_segment_codes + word['code'])
        text_match_score = jaro_similarity(text, actual_segment + word['word'])
        # new_distance = damerau_levenshtein_distance(segment_codes, actual_segment_codes + word['code'])

        len_compare_continue = len(text) / len(actual_segment + word['word']) > 1.1
        len_compare_revert = len(text) / len(actual_segment + word['word']) < 0.8
        # text_compare = text_match_score > text_match 
        # print('shortness', len(text) / len(actual_segment + word['word']), text, actual_segment + word['word'])
        improved_by = new_match_score - best_match
        improved_by_text = text_match_score - text_match
        newline_condition = 0.2
        if is_new_line:
          newline_condition = -0.2
          num_lines += 1
        
        if len_compare_revert:
          fill_lines = True
          num_lines -= 1
          actual_segment = ''
          break
        # print(improved_by + improved_by_text + newline_condition, 'word', word['word'])
        # print(new_match_score + text_match_score)
        base_condition = (improved_by + improved_by_text + newline_condition) > 0 or len_compare_continue
        if base_condition:
          if new_match_score > best_match:
            best_match = new_match_score
          if text_match_score > text_match:
            text_match = text_match_score
          # distance = new_distance
          actual_segment_codes += word['code']
          actual_segment += word['word']
          actual_segment_codes += ' '
          actual_segment += ' '
        else:
          remaining_words = remaining_words[i:]
          break
        
    processed_lines = 0
    if fill_lines:
      if num_lines == 0:
        num_lines = 1
      for i,word in enumerate(remaining_words):
        if len(word["word"]) > 0:
          is_new_line = word['newline']
          if is_new_line:
            processed_lines += 1
          
          # print('processed_lines', processed_lines, 'num_lines', num_lines)
          if processed_lines > num_lines:
            remaining_words = remaining_words[i:]
            break

          actual_segment += word['word']
          actual_segment += ' '

      # print('other segment', actual_segment)
          

    result.append({
      "text": segment["text"],
      "start": segment['start'],
      "end": segment['end'],
      "words": replace_words.replace_words(actual_segment.strip(), nums=segment['words'])
    })
  save_file('text_replaced.txt', parse_words_to_text(result))
  return result

def parse_segments_from_file(filename):
  f = open(filename)
  data = json.load(f)

  return data['segments']

def parse_words_to_text(segments):
  result = ''
  for segment in segments:
    for word in segment['words']:
      result += word['word'].strip()
      result += ' '
    result += '\n'
  return result

def save_file(filename, content):
  f = open(filename, "a")
  f.write(content)
  f.close()

# match_text(parse_segments_from_file('transcript_bela_medium.json'), 'actual_lyrics.txt')
# save_file('text_transcribed.txt', parse_words_to_text(parse_segments_from_file('transcript_bela_medium.json')))


