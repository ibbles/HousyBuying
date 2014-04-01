#!/usr/bin/python


import json
import random


class Point(object):
  x = 0.0
  y = 0.0

  def __init__(self, x, y):
    self.x = x
    self.y = y


  def add(self, other):
    self.x += other.x
    self.y += other.y




class Swarm(object):
  points = []

  def __init__(self, numPoints):
    for i in range(0, numPoints):
      self.points.append(Point(random.random(), random.random()))





class BoundCalculator(object):
  swarm = None
  upperBound = None
  lowerBound = None

  def __init__(self, swarm):
    self.swarm = swarm


  def bound(self):
    maxX = 0.0
    maxY = 0.0
    minX = 1.0
    minY = 1.0

    for point in self.swarm.points:
      minX = point.x if point.x < minX else minX
      minY = point.y if point.y < minY else minY
      maxX = point.x if point.x > maxX else maxX
      maxY = point.y if point.y > maxY else maxY

    self.upperBound = Point(maxX, maxY)
    self.lowerBound = Point(minX, minY)

    return (self.lowerBound, self.upperBound)




class MidCalculator(object):
  swarm = None
  mid = None

  def __init__(self, swarm):
    self.swarm = swarm


  def mid(self):
    self.mid = Point(0.0, 0.0)

    for point in self.swarm.points:
      self.mid.add(point)

    self.mid.x /= len(self.swarm.points)
    self.mid.y /= len(self.swarm.points)

    return self.mid



swarm = Swarm(10)
boundCalculator = BoundCalculator(swarm)
midCalculator = MidCalculator(swarm)

bound = boundCalculator.bound()
mid = midCalculator.mid()

print("Bound: ({}, {}) -> ({}, {}).".format(bound[0].x, bound[0].y, bound[1].x, bound[1].y))
print("Mid: ({}, {}).".format(mid.x, mid.y))


print("BoundCalculater: <{}>".format(json.dumps(boundCalculator)))
print("MidCalculator: <{}>".format(json.dumps(midCalculator)))

