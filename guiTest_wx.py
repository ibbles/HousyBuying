#!/usr/bin/python


# Imports for my own classes.
from NumberSequences import NumberList

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
from matplotlib.dates import date2num
from datetime import date
from datetime import datetime
from datetime import timedelta



class RateFrame(wx.Frame):
  def __init__(self, interestRates):
    self.dragging = False
    self.draggedIndex = -1
    self.clicktime = datetime.now()
    self.annotation = None

    self.interestRates = interestRates
    self.copyRatesToPlotData()


    wx.Frame.__init__(self, None, -1, 'Rate configuration')
    self.curvePanel = wx.Panel(self)
    self.figure = Figure()
    self.axes = self.figure.add_subplot(111)
    self.axes.set_title('Rates')
    self.figure.autofmt_xdate()
    self.curve = self.axes.plot(self.plotData[0], self.plotData[1], marker='o', picker=5)[0]
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
    self.canvas.mpl_connect('button_press_event', self.onclick)


  def copyRatesToPlotData(self):
    self.plotData = ([], [])
    for datePoint,rate in self.interestRates:
      self.plotData[0].append(datePoint)
      self.plotData[1].append(rate)

  def copyPlotDataToRates(self):
    self.interestRates = NumberList([])
    for index in range(0, self.getNumPlotPoints()):
      self.interestRates.insert(self.getPlotDateRate(index))

  def getNumPlotPoints(self):
    if len(self.plotData[0]) != len(self.plotData[1]):
      return None
    return len(self.plotData[0])

  def getPlotDate(self, index):
    return self.plotData[0][index]

  def getPlotRate(self, index):
    return self.plotData[1][index]

  def getPlotDateRate(self, index):
    return (self.getPlotDate(index), self.getPlotRate(index))


  def drawRates(self):
    self.curve.set_xdata(self.plotData[0])
    self.curve.set_ydata(self.plotData[1])

    if self.dragging:
      if self.annotation != None:
        self.annotation.remove()
      self.annotation = self.axes.annotate("{0}  -  {1}%".format(
                          self.plotData[0][self.draggedIndex], self.plotData[1][self.draggedIndex]),
                          xy=(self.plotData[0][self.draggedIndex], self.plotData[1][self.draggedIndex]))

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
      self.plotData[0][self.draggedIndex] = self.roundDate(withtime)
      self.plotData[1][self.draggedIndex] = self.roundRate(event.ydata)
      while self.draggedIndex+1 < len(self.plotData[0]) and self.plotData[0][self.draggedIndex] > self.plotData[0][self.draggedIndex+1]:
        self.plotData[0][self.draggedIndex], self.plotData[0][self.draggedIndex+1] = self.plotData[0][self.draggedIndex+1], self.plotData[0][self.draggedIndex]
        self.plotData[1][self.draggedIndex], self.plotData[1][self.draggedIndex+1] = self.plotData[1][self.draggedIndex+1], self.plotData[1][self.draggedIndex]
        self.draggedIndex += 1
      while self.draggedIndex > 0 and self.plotData[0][self.draggedIndex] < self.plotData[0][self.draggedIndex-1]:
        self.plotData[0][self.draggedIndex], self.plotData[0][self.draggedIndex-1] = self.plotData[0][self.draggedIndex-1], self.plotData[0][self.draggedIndex]
        self.plotData[1][self.draggedIndex], self.plotData[1][self.draggedIndex-1] = self.plotData[1][self.draggedIndex-1], self.plotData[1][self.draggedIndex]
        self.draggedIndex -= 1
      self.drawRates()


  def onrelease(self, event):
    print("onrelease")
    if self.annotation != None:
      # A point has been moved.
      self.annotation.remove()
      self.annotation = None
      self.dragging = False
      self.draggedIndex = -1
      self.copyPlotDataToRates()
      self.copyRatesToPlotData() # For testing only. Should not be needed.
    self.drawRates()

  def onclick(self, event):
    print("onclick")
    now = datetime.now()
    elapsed = now - self.clicktime
    doubleClickTime = timedelta(milliseconds=200)
    if elapsed < doubleClickTime:
      newDate = self.roundDate(num2date(event.xdata))
      newRate = self.roundRate(event.ydata)
      print("Double click on {0} x {1}".format(newDate, newRate))


    self.clicktime = now


  def roundRate(self, rate):
    return round(rate*2)/2

  def roundDate(self, dateToRound):
    return date(dateToRound.year, dateToRound.month, 1)


if __name__ == '__main__':
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

  app = wx.PySimpleApp()
  app.frame = RateFrame(NumberList(interestAtDate_data));
  app.frame.Show()
  app.MainLoop()