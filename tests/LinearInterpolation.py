#!/usr/bin/python

import sys

sys.path.append('./')

from NumberSequences import DateNumberList
from NumberSequences import LinearInterpolation

from datetime import date

dateToInterestTable = DateNumberList([
  (date(1,1,1), 0.0),
  (date(1,1,20), 1.0),
  (date(1,1,30), 2.0)
])


linearInterpolation = LinearInterpolation(dateToInterestTable)

for day in range(1,32):
  print(linearInterpolation.getNumber(date(1,1,day)))