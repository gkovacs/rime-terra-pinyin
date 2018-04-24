#!/usr/bin/env python3

seen_start = False
lines = open('orig_files/terra_pinyin.dict.yaml').readlines()
data_lines = []
start_lines = []
for line in lines:
  line = line.strip()
  if line == '...':
    seen_start = True
    start_lines.append(line)
    continue
  if not seen_start:
    start_lines.append(line)
    continue
  data_lines.append(line)

fanti_to_pinyin_list_cedict = {}
fanti_to_pinyin_list_terra = {}
fanti_to_pinyin_to_percent_terra = {}
fanti_list = []

for line in data_lines:
  if '\t' not in line:
    continue
  line_items = line.split('\t')
  fanti = None
  pinyin = None
  percent = None
  if len(line_items) == 2:
    [fanti, pinyin] = line_items
  elif len(line_items) == 3:
    [fanti, pinyin, percent] = line_items
  else:
    raise 'line items wrong length ' + line
  pinyin = pinyin.lower()
  if fanti not in fanti_to_pinyin_list_terra:
    fanti_list.append(fanti)
    fanti_to_pinyin_list_terra[fanti] = []
  fanti_to_pinyin_list_terra[fanti].append(pinyin)
  if percent != None:
    if fanti not in fanti_to_pinyin_to_percent_terra:
      fanti_to_pinyin_to_percent_terra[fanti] = {}
    fanti_to_pinyin_to_percent_terra[fanti][pinyin] = percent

cedict_lines = open('orig_files/cedict_ts.u8').readlines()
cedict_lines = [x for x in cedict_lines if not x.startswith('#')]
for line in cedict_lines:
  if ' ' not in line:
    continue
  fanti = line.split(' ')[0]
  pinyin_start_idx = line.index('[')
  pinyin_end_idx = line.index(']')
  pinyin = line[pinyin_start_idx + 1 : pinyin_end_idx]
  pinyin = pinyin.lower()
  if fanti not in fanti_to_pinyin_list_cedict:
    fanti_to_pinyin_list_cedict[fanti] = []
  fanti_to_pinyin_list_cedict[fanti].append(pinyin)

data_lines_new = []
for fanti in fanti_list:
  pinyin_list_terra = fanti_to_pinyin_list_terra[fanti]
  pinyin_list = []
  if fanti in fanti_to_pinyin_list_cedict:
    pinyin_list = fanti_to_pinyin_list_cedict[fanti]
  pinyin_set = set(pinyin_list)
  for pinyin in pinyin_list_terra:
    if pinyin not in pinyin_set:
      pinyin_list.append(pinyin)
      pinyin_set.add(pinyin)
  for pinyin in pinyin_list:
    percent = None
    if (fanti in fanti_to_pinyin_to_percent_terra) and (pinyin in fanti_to_pinyin_to_percent_terra[fanti]):
      percent = fanti_to_pinyin_to_percent_terra[fanti][pinyin]
    if percent == None:
      data_lines_new.append(fanti + '\t' + pinyin)
    else:
      data_lines_new.append(fanti + '\t' + pinyin + '\t' + percent)

for line in start_lines:
  print(line)
for line in data_lines_new:
  print(line)
