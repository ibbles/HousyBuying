
import matplotlib
import matplotlib.pyplot as pyplot
from matplotlib.pyplot import figure as Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas

import datetime
from datetime import date
import sys
import wx

class GraphFrame(wx.Frame):
  def __init__(self, title):
    wx.Frame.__init__(self, None, -1, title)
    self.Bind(wx.EVT_CLOSE, self.onWindowClose)

    self.graphPanel = wx.Panel(self)
    self.figure = Figure()
    self.axes = self.figure.add_subplot(111)
    self.axes.set_title(title)
    self.axes.grid(True, 'major')
    self.curves = []
    self.figure.autofmt_xdate()

    self.clearLimits()

    self.canvas = FigCanvas(self.graphPanel, -1, self.figure)
    self.vbox = wx.BoxSizer(wx.VERTICAL)
    self.vbox.Add(self.canvas, 1, flag=wx.LEFT|wx.TOP|wx.GROW)

    self.graphPanel.SetSizer(self.vbox)
    self.vbox.Fit(self.graphPanel)
    self.Fit()


  def onWindowClose(self, event):
    self.Hide()


  def clearLimits(self):
    self.minDate = date(datetime.MAXYEAR, 12, 31)
    self.maxDate = date(datetime.MINYEAR,  1,  1)
    self.minValue = 0
    self.maxValue = -sys.float_info.max



  def updateLimits(self, dates, values):
    minDate = dates[0]
    if minDate < self.minDate:
      self.minDate = minDate

    maxDate = dates[len(dates)-1]
    if maxDate > self.maxDate:
      self.maxDate = maxDate

    minValue = min(values)
    if minValue < self.minValue:
      self.minValue = minValue

    maxValue = max(values)* 1.1
    if maxValue > self.maxValue:
      self.maxValue = maxValue


  def clearCurves(self):
    for curve in self.curves:
      curve.remove()
    del self.curves[:]


  def clearGraph(self):
    self.clearCurves()
    self.clearLimits()


  def addGraph(self, dates, values, color):
    assert len(dates) == len(values)
    if color == None:
      color = 'b'

    self.updateLimits(dates, values);
    
    self.axes.set_ylim(bottom=self.minValue, top=self.maxValue)
    self.axes.set_xlim(left=self.minDate, right=self.maxDate)
    self.curves.append(self.axes.plot(dates, values, color=color)[0])


  def setGraph(self, dates, values):
    self.clearGraph()
    self.addGraph(dates, values)    
    self.canvas.draw()


  def setGraphs(self, dates, values, colors):
    assert len(dates) == len(values)
    assert len(dates) == len(colors)
    self.clearGraph()
    for i in range(0, len(dates)):
      self.addGraph(dates[i], values[i], colors[i])
    self.canvas.draw()

