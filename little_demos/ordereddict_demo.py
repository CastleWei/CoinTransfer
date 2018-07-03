from collections import OrderedDict

d = OrderedDict()
# 按插入顺序
d['d'] = 9
d['b'] = 10
d['a'] = 1
d['c'] = 8
for letter in d:
  print(letter)