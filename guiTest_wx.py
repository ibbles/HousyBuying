#!/usr/bin/python

import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas
import numpy
import wx



class RateFrame(wx.Frame):
  def __init__(self):
    self.xData = [5, 6, 5, 6, 7]
    wx.Frame.__init__(self, None, -1, 'Rate configuration')
    self.curvePanel = wx.Panel(self)
    self.figure = Figure()
    self.axes = self.figure.add_subplot(111)
    self.axes.set_title('Rates')
    self.plotData = self.axes.plot(self.xData)[0]

    self.canvas = FigCanvas(self.curvePanel, -1, self.figure)
  
    self.vbox = wx.BoxSizer(wx.VERTICAL)
    self.vbox.Add(self.canvas, 1, flag=wx.LEFT | wx.TOP | wx.GROW)
    self.curvePanel.SetSizer(self.vbox)
    self.vbox.Fit(self)

    self.drawRates()

  def drawRates(self):
    self.axes.set_xbound(lower=0, upper=5)
    self.axes.set_ybound(lower=0, upper=10)
    self.plotData.set_xdata(numpy.arange(len(self.xData)))
    self.plotData.set_ydata(self.xData)

    self.canvas.draw();



if __name__ == '__main__':
  app = wx.PySimpleApp()
  app.frame = RateFrame();
  app.frame.Show()
  app.MainLoop()