


# Imports for my own classes.
from NumberSequences import DateNumberList
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
import math
from matplotlib.dates import num2date
from matplotlib.dates import date2num
from datetime import date
from datetime import datetime
from datetime import timedelta







class CurveFrame(wx.Frame):
  """
  A CurveFrame provides a way for the user to input numbers that vary over time.
  """

  dateNumberList = None
  """
  List of control points that the user can manipulate. This object is shared
  with some other, lower-level, object that reads the number for some purpose.
  The account interest and savings are examples of this.
  """

  defaultValue = None
  """Value that will be added if the list would become empty for some reason."""

  maxValue = None
  """The current extent of the Y-axis. Number rounding is done in relation to this."""

  unit = None
  """Text string placed after values when printing. Common ones are 'kr' and '%'."""



  def __init__(self, dateNumberList, defaultValue, maxValue, unit, title):
    self.dateNumberList = dateNumberList
    self.defaultValue = defaultValue
    self.maxValue = maxValue
    self.unit = unit
    self.userFirstDate = dateNumberList.getFirstDate()
    self.userLastDate = dateNumberList.getLastDate()

    self.initClickState();
    self.initPlotData();
    self.initFrame(title);
    self.initCallbacks();

    self.drawNumbers()

    self.sanityCheck()

  def setYearRange(self, startYear, endYear):
    self.userFirstDate = startYear
    self.userLastDate = endYear
    if self.userFirstDate.year == self.userLastDate.year:
      self.userLastDate = date(self.userLastDate.year+1, 1, 1)
    if self.userFirstDate > self.userLastDate:
      self.userFirstDate, self.userLastDate = self.userLastDate, self.userFirstDate

    listChanged = False
    firstDate = self.dateNumberList.getFirstDate()
    firstValue = self.dateNumberList.getFirstNumber()
    if firstDate == None or firstDate > self.userFirstDate:
      newValue = self.defaultValue if firstValue == None else firstValue
      self.dateNumberList.insert((self.userFirstDate, newValue))
      listChanged = True

    lastDate = self.dateNumberList.getLastDate()
    lastValue = self.dateNumberList.getLastNumber()
    if lastDate == None or lastDate < self.userLastDate:
      newValue = self.defaultValue if lastValue == None else lastValue
      self.dateNumberList.insert((self.userLastDate, newValue))
      listChanged = True

    if listChanged:
      self.copyNumbersToPlotData()

    self.drawNumbers()


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
    self.vbox.Fit(self.curvePanel)
    self.Fit()

    self.Bind(wx.EVT_CLOSE, self.onWindowClose)


  def onWindowClose(self, event):
    self.Hide()



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
    self.dateNumberList.clear()
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
    self.axes.set_ylim(0.0, self.maxValue)
    # self.axes.set_yticks(range(0, self.maxValue)) # Must not be hard coded.

    self.curve.set_xdata(self.plotData.dates)
    self.curve.set_ydata(self.plotData.numbers)

    if self.dragging:
      if self.annotation != None:
        self.annotation.remove()
      index = self.draggedIndex
      datePoint = self.getPlotDate(index)
      number = self.getPlotNumber(index)
      if math.modf(number/100)[0] == 0:
        number = int(number)

      annotateDate = self.calculateAnnotateDate(lowerDate, upperDate, datePoint)
      self.annotation = self.axes.annotate("{0}  -  {1}{2}".format(datePoint, number, self.unit), xy=(annotateDate, number))

    self.canvas.draw()

    self.sanityCheck()

  def calculateAnnotateDate(self, lowerDate, upperDate, datePoint):
    # TODO How do I find these number properly?
    fractionUsedForPlot = 0.8
    charactersInAnnotation = 4+1+2+1+2 + 3 + 5+3 # year, dash, month, dash, day, wide dash, number, unit.
    annotationWidthInPixels = self.GetCharWidth()*charactersInAnnotation
    widthInPixels = self.GetClientSizeTuple()[0] * fractionUsedForPlot
    widthInSeconds = (upperDate - lowerDate).total_seconds()
    secondsPerPixel = widthInSeconds / widthInPixels;
    annotationWidthInSeconds = annotationWidthInPixels * secondsPerPixel

    maxDate = upperDate - timedelta(seconds=annotationWidthInSeconds)
    if datePoint > maxDate:
      return maxDate
    else:
      return datePoint


  def calculateDateRange(self):
    dataFirstDate = self.dateNumberList.getFirstDate()
    dataLastDate = self.dateNumberList.getLastDate()
    if dataFirstDate != None:
      dataFirstDate = self.roundDateDown(dataFirstDate)
    if dataLastDate != None:
      dataLastDate = self.roundDateUp(dataLastDate)

    firstDate = self.selectSmallest(dataFirstDate, self.userFirstDate)
    lastDate = self.selectLargest(dataLastDate, self.userLastDate)

    today = date.today()
    if firstDate == None:
      firstDate = date(today.year, 1, 1)
    if lastDate == None:
      lastDate = date(today.year+1, 1, 1)

    if firstDate > lastDate:
      firstDate, lastDate = lastDate, firstDate

    return (firstDate, lastDate)


  def selectSmallest(self, first, second):
    if first != None and second != None:
      return first if first < second else second
    elif first != None:
      return first
    elif second != None:
      return second
    else:
      return None


  def selectLargest(self, first, second):
    if first != None and second != None:
      return first if first > second else second
    elif first != None:
      return first
    elif second != None:
      return second
    else:
      return None



  def onpick(self, pickEvent):
    # Only want one index. The event may contain a list of them.
    index = pickEvent.ind
    if not isinstance(index, int):
      index = index[0]
    if pickEvent.mouseevent.xdata == None or pickEvent.mouseevent.ydata == None:
      return

    index = self.findClosest(index, self.stripTime(num2date(pickEvent.mouseevent.xdata)))
    # The button used determines the action to perform.
    button = pickEvent.mouseevent.button
    if button == 1:
      # Prepare to move a line joint.
      thisline = pickEvent.artist
      xdata = thisline.get_xdata()
      ydata = thisline.get_ydata()
      self.dragging = True
      self.draggedIndex = index
      self.drawNumbers()
    else:
      if index == 0 or index == self.dateNumberList.getLastIndex():
        return
      # Remove a joint.
      self.dateNumberList.delete(index)
      self.copyNumbersToPlotData()
      self.drawNumbers()

    self.sanityCheck()


  def findClosest(self, index, datePoint):
    next = index + 1
    if self.dateNumberList.isValidIndex(next):
      indexDate = self.dateNumberList.getDate(index);
      nextDate = self.dateNumberList.getDate(next);
      indexDelta = datePoint - indexDate
      nextDelta = datePoint - nextDate
      indexSeconds = math.fabs(indexDelta.total_seconds())
      nextSeconds = math.fabs(nextDelta.total_seconds())
      return index if indexSeconds <= nextSeconds else next
    else:
      return index


  def onmotion(self, mouseEvent):
    if mouseEvent.xdata == None or mouseEvent.ydata == None:
      return # Happens when mouse is moved outside of the plotting area.
    if self.dragging:
      self.sanityCheck()
      withtime = num2date(mouseEvent.xdata)
      if self.draggedIndex == 0 or self.draggedIndex == self.dateNumberList.getLastIndex():
        withtime = self.dateNumberList.getDate(self.draggedIndex)
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


  def onclick(self, mouseEvent):
    isDoubleClick = self.isDoubleClick(mouseEvent)
    if mouseEvent.xdata == None or mouseEvent.ydata == None:
      return # Clicked outside of figure.
    if isDoubleClick and mouseEvent.button == 1:
      self.addPoint(mouseEvent)

    self.clickTime = datetime.now()


  def isDoubleClick(self, mouseEvent):
    now = datetime.now()
    elapsed = now - self.clickTime
    doubleClickTime = timedelta(milliseconds=200)
    return elapsed < doubleClickTime



  def addPoint(self, mouseEvent):
    newDate = self.roundDate(num2date(mouseEvent.xdata))
    newNumber = self.roundNumber(mouseEvent.ydata)
    self.dateNumberList.insert((newDate, newNumber))
    self.copyNumbersToPlotData()
    self.drawNumbers()


    self.sanityCheck()


  def stripTime(self, dateTimePoint):
    return date(dateTimePoint.year, dateTimePoint.month, dateTimePoint.day)

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
    highPrecision = wx.GetKeyState(wx.WXK_SHIFT)
    precision = self.getPrecision(self.maxValue, highPrecision)
    return round(number/precision)*precision


  def getPrecision(self, number, highPrecision):
    if number == 0:
      return 0
    if number < 1:
      return number/10.0
    magnitude = 1
    walker = number
    while walker >= 1:
      magnitude *= 10
      walker /= 10.0

    if highPrecision:
      precisions = [1000.0, 1000.0, 1000.0, 1000.0]
    else:
      precisions = [1000.0, 500.0, 200.0, 100.0]

    if number <= 0.25 * magnitude:
      precision = magnitude / precisions[0]
    elif number <= 0.50 * magnitude:
      precision = magnitude / precisions[1]
    elif number <= 0.75 * magnitude:
      precision = magnitude / precisions[2]
    else:
      precision = magnitude / precisions[3]
    if highPrecision:
      precision /= 10.0
    return precision




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
