#!/usr/bin/python


# Imports required for plotting.
import matplotlib
import matplotlib.pyplot as pyplot
from matplotlib.pyplot import figure as Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas

# Imports required for GUI.
import wx

# Utility functions
import numpy
from matplotlib.dates import num2date
from datetime import date
from datetime import datetime


interestAtDate_data = [
  (date(2014, 1, 1), 3.0),
  (date(2014, 2, 1), 2.0),
  (date(2014, 3, 1), 3.0),
  (date(2014, 4, 1), 4.0),
  (date(2014, 5, 1), 3.0),
  (date(2015, 3, 1), 4.0),
  (date(2015, 8, 1), 5.0),
  (date(2016, 2, 1), 6.0),
  (date(2016, 5, 1), 7.0)
]
plotData = ([], [])
for datePoint,rate in interestAtDate_data:
  plotData[0].append(datePoint)
  plotData[1].append(rate)

class RateFrame(wx.Frame):
  def __init__(self):
    self.dragging = False
    self.draggedIndex = -1
    self.annotation = None

    wx.Frame.__init__(self, None, -1, 'Rate configuration')
    self.curvePanel = wx.Panel(self)
    self.figure = Figure()
    self.axes = self.figure.add_subplot(111)
    self.axes.set_title('Rates')
    self.figure.autofmt_xdate()
    self.curve = self.axes.plot(plotData[0], plotData[1], marker='o', picker=5)[0]
    self.axes.set_xlim(date(2014, 1, 1), date(2016, 12, 1))
    self.axes.set_ylim(0.0, 10.0)
    self.axes.set_yticks(range(0, 11))
    self.axes.grid(True, 'major')

    self.canvas = FigCanvas(self.curvePanel, -1, self.figure)
  
    self.vbox = wx.BoxSizer(wx.VERTICAL)
    self.vbox.Add(self.canvas, 1, flag=wx.LEFT | wx.TOP | wx.GROW)
    self.curvePanel.SetSizer(self.vbox)
    self.vbox.Fit(self)

    self.drawRates()

    self.canvas.mpl_connect('pick_event', self.onpick)
    self.canvas.mpl_connect('button_release_event', self.onrelease)
    self.canvas.mpl_connect('motion_notify_event', self.onmotion)

  def drawRates(self):
    self.curve.set_xdata(plotData[0])
    self.curve.set_ydata(plotData[1])

    if self.dragging:
      if self.annotation != None:
        self.annotation.remove()
      self.annotation = self.axes.annotate("{0}  -  {1}%".format(
                          plotData[0][self.draggedIndex], plotData[1][self.draggedIndex]),
                          xy=(plotData[0][self.draggedIndex], plotData[1][self.draggedIndex]))

    self.canvas.draw();



  def onpick(self, event):
    print("onpick")
    thisline = event.artist
    xdata = thisline.get_xdata()
    ydata = thisline.get_ydata()
    index = event.ind
    self.dragging = True
    if isinstance(index, int):
      self.draggedIndex = index
    else:
      self.draggedIndex = index[0]
    self.drawRates()


  def onmotion(self, event):
    if self.dragging:
      withtime = num2date(event.xdata)
      plotData[0][self.draggedIndex] = date(withtime.year, withtime.month, 1)
      plotData[1][self.draggedIndex] = round(event.ydata*2+0.5)/2
      while self.draggedIndex+1 < len(plotData[0]) and plotData[0][self.draggedIndex] > plotData[0][self.draggedIndex+1]:
        plotData[0][self.draggedIndex], plotData[0][self.draggedIndex+1] = plotData[0][self.draggedIndex+1], plotData[0][self.draggedIndex]
        plotData[1][self.draggedIndex], plotData[1][self.draggedIndex+1] = plotData[1][self.draggedIndex+1], plotData[1][self.draggedIndex]
        self.draggedIndex += 1
      while self.draggedIndex > 0 and plotData[0][self.draggedIndex] < plotData[0][self.draggedIndex-1]:
        plotData[0][self.draggedIndex], plotData[0][self.draggedIndex-1] = plotData[0][self.draggedIndex-1], plotData[0][self.draggedIndex]
        plotData[1][self.draggedIndex], plotData[1][self.draggedIndex-1] = plotData[1][self.draggedIndex-1], plotData[1][self.draggedIndex]
        self.draggedIndex -= 1
      self.drawRates()


  def onrelease(self, event):
    print("onrelease")
    self.dragging = False
    self.draggedIndex = -1
    if self.annotation != None:
      self.annotation.remove()
      self.annotation = None
    self.drawRates()



if __name__ == '__main__':
  app = wx.PySimpleApp()
  app.frame = RateFrame();
  app.frame.Show()
  app.MainLoop()