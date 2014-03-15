


# Imports for my own classes.
from NumberSequences import NumberList
from NumberSequences import getDate
from NumberSequences import getNumber

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



class CurveFrame(wx.Frame):
  def __init__(self, dateNumberList, title):
    self.dateNumberList = dateNumberList;
    self.initClickState();
    self.initPlotData();
    self.initFrame(title);
    self.initCallbacks();

    self.drawNumbers()

    self.sanityCheck()


  def initFrame(self, title):
    wx.Frame.__init__(self, None, -1, title)
    self.curvePanel = wx.Panel(self)
    self.figure = Figure();
    self.axes = self.figure.add_subplot(111)
    self.axes.set_title(title)
    self.figure.autofmt_xdate()
    self.curve = self.axes.plot(self.plotData.dates, self.plotData.numbers, marker='o', picker=5)[0]
    self.axes.grid(True, 'major')

    self.canvas = FigCanvas(self.curvePanel, -1, self.figure)

    self.vbox = wx.BoxSizer(wx.VERTICAL)
    self.vbox.Add(self.canvas, 1, flag=wx.LEFT|wx.TOP|wx.GROW)
    self.curvePanel.SetSizer(self.vbox)
    self.vbox.Fit(self)



  def initPlotData(self):
    self.plotData = type('PlotData', (object,), {'dates' : [], 'numbers' : []})()
    self.copyNumbersToPlotData()
    


  def initClickState(self):
    self.dragging = False
    self.draggedIndex = -1
    self.clickTime = datetime.now()
    self.annotation = None



  def initCallbacks(self):
    self.canvas.mpl_connect('pick_event', self.onpick)
    self.canvas.mpl_connect('motion_notify_event', self.onmotion)
    self.canvas.mpl_connect('button_press_event', self.onclick)
    self.canvas.mpl_connect('button_release_event', self.onrelease)



  def copyNumbersToPlotData(self): # Consider using list comprehensions here.
    self.plotData.dates = []
    self.plotData.numbers = []
    for datePoint,number in self.dateNumberList:
      if datePoint == None: raise Exception()
      if number == None: raise Exception()
      self.plotData.dates.append(datePoint)
      self.plotData.numbers.append(number)

    self.sanityCheck()


  def copyPlotDataToNumbers(self):  # Consider using list comprehensions here.
    self.dateNumberList = NumberList([])
    for index in range(0, self.getNumPlotPoints()):
      self.dateNumberList.insert(self.getPlotDateNumber(index))

    self.sanityCheck()


  def getNumPlotPoints(self):
    if len(self.plotData.dates) != len(self.plotData.numbers):
      return None
    return len(self.plotData.dates)


  def getPlotDate(self, index):
    if index < 0 or index >= len(self.plotData.dates):
      return None
    return self.plotData.dates[index]


  def getPlotNumber(self, index):
    if index < 0 or index >= len(self.plotData.dates):
      return None
    return self.plotData.numbers[index]


  def getPlotDateNumber(self, index):
    if index < 0 or index >= self.getNumPlotPoints():
      return None
    return (self.getPlotDate(index), self.getPlotNumber(index))



  def drawNumbers(self):
    self.sanityCheck()

    lowerDate, upperDate = self.calculateDateRange()
    self.axes.set_xlim(lowerDate, upperDate)
    self.axes.set_ylim(0.0, 10.0) # Must not be hard coded.
    self.axes.set_yticks(range(0, 11)) # Must not be hard coded.

    self.curve.set_xdata(self.plotData.dates)
    self.curve.set_ydata(self.plotData.numbers)

    if self.dragging:
      if self.annotation != None:
        self.annotation.remove()
      index = self.draggedIndex
      datePoint = self.getPlotDate(index)
      number = self.getPlotNumber(index)
      self.annotation = self.axes.annotate("{0}  -  {1}%".format(datePoint, number), xy=(datePoint, number))

    self.canvas.draw()

    self.sanityCheck()


  def calculateDateRange(self):
    firstDate = self.dateNumberList.getFirstDate()
    lastDate = self.dateNumberList.getLastDate()
    today = date.today()
    if firstDate == None:
      firstDate = today
    if lastDate == None:
      lastDate = today
    return (self.roundDateDown(firstDate), self.roundDateUp(lastDate))



  def onpick(self, pickEvent):
    button = pickEvent.mouseevent.button
    if button == 1:
      # Prepare to move a line joint.
      thisline = pickEvent.artist
      xdata = thisline.get_xdata()
      ydata = thisline.get_ydata()
      index = pickEvent.ind
      self.dragging = True
      if isinstance(index, int):
        self.draggedIndex = index
      else:
        self.draggedIndex = index[0]
      self.drawNumbers()
    else:
      # Remove a joint.
      index = pickEvent.ind
      self.dateNumberList.delete(index)
      self.copyNumbersToPlotData()
      self.drawNumbers()

    self.sanityCheck()


  def onmotion(self, mouseEvent):
    if mouseEvent.xdata == None or mouseEvent.ydata == None:
      return # Happens when mouse is moved outside of the plotting area.
    if self.dragging:
      self.sanityCheck()
      withtime = num2date(mouseEvent.xdata)
      self.plotData.dates[self.draggedIndex] = self.roundDate(withtime)
      self.plotData.numbers[self.draggedIndex] = self.roundNumber(mouseEvent.ydata)
      self.draggedIndex = self.bubble(self.draggedIndex)
      self.copyPlotDataToNumbers() # Not really needed.
      self.drawNumbers()

      self.sanityCheck()


  def onrelease(self, mouseEvent):
    if self.dragging:
      # A point has been removed.
      if self.annotation != None:
        self.annotation.remove()
        self.annotation = None
      self.dragging = False
      self.draggedIndex = -1
      self.copyPlotDataToNumbers()
      self.copyNumbersToPlotData() # For data integrity only. Should not be needed.
    self.drawNumbers()

    self.sanityCheck()


 # Can get None or something on x/y data here. Use to detect out-of-bounds click and extend x range in that direction.
  def onclick(self, mouseEvent): 
    now = datetime.now()
    elapsed = now - self.clickTime
    doubleClickTime = timedelta(milliseconds=200)
    if elapsed < doubleClickTime:
      newDate = self.roundDate(num2date(mouseEvent.xdata))
      newNumber = self.roundNumber(mouseEvent.ydata)
      self.dateNumberList.insert((newDate, newNumber))
      self.copyNumbersToPlotData()
      self.drawNumbers()

    self.clickTime = now

    self.sanityCheck()


  def roundDate(self, datePoint):
    if datePoint.day < 15: # All months have 30-ish days.
      return date(datePoint.year, datePoint.month, 1)
    elif datePoint.month < 12:
      return date(datePoint.year, datePoint.month+1, 1)
    else:
      return date(datePoint.year+1, 1, 1)


  def roundDateUp(self, datePoint):
    if datePoint.month == 1 and datePoint.day == 1:
      return datePoint
    else:
      return date(datePoint.year+1, 1, 1)


  def roundDateDown(self, datePoint):
    return date(datePoint.year, 1, 1)


  def roundNumber(self, number):
    return round(number*2)/2



  def bubble(self, index):
    if self.hasSmallerAbove(index):
      return self.bubbleUp(index)
      
    if self.hasLargerBelow(index):
      return self.bubbleDown(index)

    return index

  def bubbleUp(self, index):
    while self.hasSmallerAbove(index):
      index = self.swapUp(index)
    return index

  def bubbleDown(self, index):
    while self.hasLargerBelow(index):
      index = self.swapDown(index)
    return index



  def hasSmallerAbove(self, index):
    currDate = self.getPlotDate(index)
    nextDate = self.getPlotDate(index+1)
    return nextDate != None and nextDate < currDate

  def hasLargerBelow(self, index):
    currDate = self.getPlotDate(index)
    prevDate = self.getPlotDate(index-1)
    return prevDate != None and prevDate > currDate



  def swapUp(self, index):
    next = index + 1
    self.plotData.dates[index], self.plotData.dates[next] = self.plotData.dates[next], self.plotData.dates[index]
    self.plotData.numbers[index], self.plotData.numbers[next] = self.plotData.numbers[next], self.plotData.numbers[index]
    return next


  def swapDown(self, index):
    prev = index - 1
    self.plotData.dates[index], self.plotData.dates[prev] = self.plotData.dates[prev], self.plotData.dates[index]
    self.plotData.numbers[index], self.plotData.numbers[prev] = self.plotData.numbers[prev], self.plotData.numbers[index]
    return prev



  def sanityCheck(self):
    if self.draggedIndex == None: raise Exception()
    if self.plotData.dates == None: raise Exception()
    if self.plotData.numbers == None: raise Exception()
    if self.dateNumberList == None: raise Exception()
    if len(self.plotData.dates) != len(self.plotData.numbers): raise Exception()
    if len(self.plotData.dates) != self.dateNumberList.getSize(): raise Exception()

    for index in range(0, len(self.plotData.dates)):
      if self.plotData.dates[index] == None: raise Exception()
      if self.plotData.numbers[index] == None: raise Exception()
      
      currDateNumber = self.getPlotDateNumber(index)
      if currDateNumber == None: raise Exception()
      if getDate(currDateNumber) == None: raise Exception()
      if getNumber(currDateNumber) == None: raise Exception()

      prevDateNumber = self.getPlotDateNumber(index-1)
      if prevDateNumber != None and getDate(prevDateNumber) == None: raise Exception()
      if prevDateNumber != None and getNumber(prevDateNumber) == None: raise Exception()
      if prevDateNumber != None and getDate(prevDateNumber) > getDate(currDateNumber): raise Exception()

      nextDateNumber = self.getPlotDateNumber(index+1)
      if nextDateNumber != None and getDate(nextDateNumber) == None: raise Exception()
      if nextDateNumber != None and getNumber(nextDateNumber) == None: raise Exception()
      if nextDateNumber != None and getDate(nextDateNumber) < getDate(currDateNumber): raise Exception()

      listElem = self.dateNumberList.getPair(index)
      if listElem == None: raise Exception()
      if getDate(listElem) == None: raise Exception()
      if getNumber(listElem) == None: raise Exception()
      if getDate(listElem) != getDate(currDateNumber): raise Exception()
      if getNumber(listElem) != getNumber(currDateNumber): raise Exception()

