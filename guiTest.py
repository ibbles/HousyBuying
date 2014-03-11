#!/usr/bin/python

import numpy as numpy
import matplotlib.pyplot as plot
from matplotlib.dates import num2date
from datetime import date
from datetime import datetime

# The set of points we want to plot.
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

data = ([],[])
for datePoint,rate in interestAtDate_data:
  data[0].append(datePoint)
  data[1].append(rate)
# data = ([date(2014, 1, 1), date(2014, 2, 1), date(2014, 3, 1)], numpy.random.rand(3))

# Create the ploting area.
fig = plot.figure()
ax = fig.add_subplot(111)
ax.set_xlim(date(2014, 1, 1), date(2016, 12, 1))
ax.set_ylim(0.0, 10.0)
ax.set_yticks(range(0, 11))
ax.grid(True, 'major')


# Send data to 
line = ax.plot(data[0], data[1], marker='o', picker=5)  # 5 points tolerance

dragging = False
draggedIndex = -1

def onpick(event):
    global dragging, draggedIndex
    thisline = event.artist
    xdata = thisline.get_xdata()
    ydata = thisline.get_ydata()
    ind = event.ind
    dragging = True
    if isinstance(ind, int):
        draggedIndex = ind
    else:
      draggedIndex = ind[0]

    print(ind)


def onrelease(event):
    global dragging, draggedIndex
    dragging = False
    draggedIndex = -1
    ax.clear()
    ax.plot(data[0], data[1], marker='o', picker=5)
    ax.set_xlim(date(2014, 1, 1), date(2016, 12, 1))
    ax.set_ylim(0.0, 10.0)
    ax.set_yticks(range(0, 11))
    ax.grid(True, 'major')
    fig.canvas.draw()



def onmotion(event):
  global draggedIndex
  if dragging:
    withtime = num2date(event.xdata)
    data[0][draggedIndex] = date(withtime.year, withtime.month, 1)
    data[1][draggedIndex] = round(event.ydata*2)/2
    while draggedIndex+1 < len(data[0]) and data[0][draggedIndex] > data[0][draggedIndex+1]:
      print("Dragged data {0} on index {1} past date {2} on index {3}.".format(data[0][draggedIndex], draggedIndex, data[0][draggedIndex+1], draggedIndex+1))
      tmp = data[0][draggedIndex]
      data[0][draggedIndex] = data[0][draggedIndex+1]
      data[0][draggedIndex+1] = tmp
      tmp = data[1][draggedIndex]
      data[1][draggedIndex] = data[1][draggedIndex+1]
      data[1][draggedIndex+1] = tmp
      draggedIndex = draggedIndex + 1
    while draggedIndex > 0 and data[0][draggedIndex] < data[0][draggedIndex-1]:
      print("Dragged data {0} on index {1} past date {2} on index {3}.".format(data[0][draggedIndex], draggedIndex, data[0][draggedIndex-1], draggedIndex-1))
      tmp = data[0][draggedIndex]
      data[0][draggedIndex] = data[0][draggedIndex-1]
      data[0][draggedIndex-1] = tmp
      tmp = data[1][draggedIndex]
      data[1][draggedIndex] = data[1][draggedIndex-1]
      data[1][draggedIndex-1] = tmp
      draggedIndex = draggedIndex - 1
    print(event.xdata)
    ax.clear()
    ax.plot(data[0], data[1], marker='o', picker=5)
    ax.set_xlim(date(2014, 1, 1), date(2016, 12, 1))
    ax.set_ylim(0.0, 10.0)
    ax.set_yticks(range(0, 11))
    ax.grid(True, 'major')
    plot.annotate("{0}  -  {1}%".format(data[0][draggedIndex], data[1][draggedIndex]), xy=(data[0][draggedIndex], data[1][draggedIndex]))
    fig.canvas.draw()


fig.canvas.mpl_connect('pick_event', onpick)
fig.canvas.mpl_connect('button_release_event', onrelease)
fig.canvas.mpl_connect('motion_notify_event', onmotion)

plot.show()