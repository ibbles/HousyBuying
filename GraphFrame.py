
import matplotlib
import matplotlib.pyplot as pyplot
from matplotlib.pyplot import figure as Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas

import wx

class GraphFrame(wx.Frame):
  def __init__(self, title):
    wx.Frame.__init__(self, None, -1, title)
    self.Bind(wx.EVT_CLOSE, self.onWindowClose)


  def onWindowClose(self, event):
    self.Hide()

  def setGraph(self, dates, values):
    assert len(dates) == len(values)
    for index in range(0, len(dates)):
      print("{} : {}".format(dates[index], values[index]))
