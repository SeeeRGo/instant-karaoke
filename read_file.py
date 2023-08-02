from datetime import datetime
def parse_subtitle(filename):
  file1 = open(filename, 'r')
  Lines = list(filter(lambda line: len(line.strip()) > 0, file1.readlines()))
  fmt = '%M:%S.%f'
  diffs = filter(lambda line: len(line.strip().split('-->')) > 1, Lines)
  texts = list(filter(lambda line: len(line.strip().split('-->')) == 1, Lines))
  texts = list(map(lambda str: str.strip(), texts))
  diffs = list(diffs)
  res = []
  for diff in diffs:
    dates = list(map(lambda str: datetime.strptime(str.strip(), fmt), diff.strip().split('-->')))
    res.append((dates[1] - dates[0]).seconds)

  return list(zip(res, texts))

       