from itertools import groupby

nums = [
  {"word": "one", "start": 1, "end": 2},
  {"word": "two", "start": 2, "end": 3},
  {"word": "three", "start": 3, "end": 4},
  {"word": "four", "start": 4, "end": 5},
  {"word": "five", "start": 5, "end": 6},
  {"word": "six", "start": 6, "end": 7},
  {"word": "seven", "start": 7, "end": 8},
]
nums_uneven_durations = [
  {"word": "one", "start": 0.5, "end": 2},
  {"word": "two", "start": 2, "end": 3},
  {"word": "three", "start": 3, "end": 5},
  {"word": "four", "start": 5, "end": 5.5},
  {"word": "five", "start": 5.5, "end": 6},
  {"word": "six", "start": 6, "end": 7},
  {"word": "seven", "start": 7, "end": 10},
]
nums_uneven_durations_with_pauses = [
  {"word": "one", "start": 0.5, "end": 2},
  {"word": "two", "start": 2, "end": 3},
  {"word": "three", "start": 4, "end": 5},
  {"word": "four", "start": 5, "end": 5.5},
  {"word": "five", "start": 5.5, "end": 6},
  {"word": "six", "start": 6.5, "end": 7},
  {"word": "seven", "start": 8, "end": 10},
]

def grouper(item):
    """Будем использовать эту функцию для группировки сортировки."""
    return item['index']

def replace_words(new_text, nums=nums):
  res = []
  if len(nums) > 0 and len(new_text) > 0:
    new_words = new_text.split(' ')
    total_duration = 0
    last_end = nums[0]["start"]
    non_zero_wait = []
    for i, num in enumerate(nums):
      total_duration += num["end"] - num["start"]
      wait = num['start'] - last_end
      if wait > 0:
        non_zero_wait.append({"index":i, "wait": wait })
      last_end = num['end']
    coef = len(nums) / len(new_words)
    pos_coef = 1 / coef
    non_zero_wait = groupby(sorted([{"index":round(x["index"] * pos_coef), "wait": x["wait"]} for x in non_zero_wait], key=grouper), key=grouper)
    adjusted_wait = []
    for key, group_items in non_zero_wait:
      total_wait = 0
      for item in group_items: 
        total_wait += item['wait']
      adjusted_wait.append({ "index": key, "wait": total_wait})

    current_start = nums[0]["start"]
    if coef >= 1:
      lesser_duration = 0
      for i in range(0, len(new_words)):
        lesser_duration += nums[i]["end"] - nums[i]["start"]
      
      coef = total_duration / lesser_duration
      for i,word in enumerate(new_words):
        wait = 0
        for calc_wait in adjusted_wait:
          if calc_wait["index"] == i:
            wait = calc_wait['wait']

        current_start += wait
        res.append({
          "word": word,
          "start": current_start,
          "end": current_start + (nums[i]["end"] - nums[i]["start"]) * coef,
        })
        current_start = current_start + (nums[i]["end"] - nums[i]["start"]) * coef
    else:
      shortened_nums = []
      shortened_duration = 0
      for num in nums:
        shortened_nums.append({
          "start": current_start,
          "end": current_start + (num["end"] - num["start"]) * coef,
        })
        shortened_duration += (num["end"] - num["start"]) * coef
        current_start = current_start + (num["end"] - num["start"]) * coef
      extra_words = len(new_words) - len(nums)
      extra_duration = total_duration - shortened_duration
      extra_duration_per_word = extra_duration / extra_words
      for i in range(0, extra_words):
        shortened_nums.append({
          "start": current_start,
          "end": current_start + extra_duration_per_word,
        })
        current_start = current_start + extra_duration_per_word

      current_start = shortened_nums[0]["start"]
      for i,word in enumerate(new_words):
        wait = 0
        for calc_wait in adjusted_wait:
          if calc_wait["index"] == i:
            wait = calc_wait['wait']
        current_start += wait
        res.append({
          "word": word,
          "start": current_start,
          "end": current_start + shortened_nums[i]["end"] - shortened_nums[i]["start"]
        })
        current_start = current_start + shortened_nums[i]["end"] - shortened_nums[i]["start"]
  return res
