#!/usr/bin/python

from Accounts import Account
from Interest import Interest
from Interest import InterestRate
from NumberSequences import NumberList
from CurveFrame import CurveFrame

import datetime

import wx



import sys
def info(type, value, tb):
   if hasattr(sys, 'ps1') or not sys.stderr.isatty():
      # we are in interactive mode or we don't have a tty-like
      # device, so we call the default hook
      sys.__excepthook__(type, value, tb)
   else:
      import traceback, pdb
      # we are NOT in interactive mode, print the exception...
      traceback.print_exception(type, value, tb)
      print
      # ...then start the debugger in post-mortem mode.
      pdb.pm()

sys.excepthook = info


interestAtDate_data = [
  (datetime.date(2014, 1, 1), 1.0),
  (datetime.date(2014, 2, 1), 1.0),
  (datetime.date(2014, 3, 1), 1.0),
  (datetime.date(2014, 4, 1), 1.0),
  (datetime.date(2014, 5, 1), 1.0),
  (datetime.date(2015, 3, 1), 1.0),
  (datetime.date(2015, 8, 1), 1.0),
  (datetime.date(2016, 2, 1), 1.0),
  (datetime.date(2016, 5, 1), 1.0)
]

app = wx.PySimpleApp()
app.frame = CurveFrame(NumberList([]), 'Interest rate')
app.frame.Show()
secondFrame = CurveFrame(NumberList([]), 'Money')
secondFrame.Show(True)
app.MainLoop()