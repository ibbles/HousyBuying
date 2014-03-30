
import matplotlib
import matplotlib.pyplot as pyplot
from matplotlib.pyplot import figure as Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas

import wx

class GraphFrame(wx.Frame):
  def __init__(self, title):
    wx.Frame.__init__(self, None, -1, title)
    self.Bind(wx.EVT_CLOSE, self.onWindowClose)

    self.graphPanel = wx.Panel(self)
    self.figure = Figure()
    self.axes = self.figure.add_subplot(111)
    self.axes.set_title(title)
    self.figure.autofmt_xdate()

    self.canvas = FigCanvas(self.graphPanel, -1, self.figure)
    self.vbox = wx.BoxSizer(wx.VERTICAL)
    self.vbox.Add(self.canvas, 1, flag=wx.LEFT|wx.TOP|wx.GROW)

    self.graphPanel.SetSizer(self.vbox)
    self.vbox.Fit(self.graphPanel)
    self.Fit()


  def onWindowClose(self, event):
    self.Hide()

  def setGraph(self, dates, values):
    assert len(dates) == len(values)

    self.curve = self.axes.plot(dates, values)[0]
    self.canvas.draw()

    for index in range(0, len(dates)):
      print("{} : {}".format(dates[index], values[index]))
