
def getDate(dateNumber):
  return dateNumber[0]

def getNumber(dateNumber):
  return dateNumber[1]



class DateNumberList(object):
  """A NumberList is a sorted list of date-number pairs."""

  def __init__(self, list):
    self.__list = sorted(list, key = lambda entry: entry[0])

  def insert(self, dateNumber):
    # Handle corner cases first so that the while-loop berlow becomes easier.
    if self.getSize() == 0:
      self.__list.append(dateNumber)
      return
    if self.getLastDate() < getDate(dateNumber):
      self.__list.append(dateNumber)
      return
    if self.getFirstDate() > getDate(dateNumber):
      self.__list.insert(0, dateNumber)
      return
    # We now know that the new dateNumber will go to a valid index of the list.
    # \todo The list is sorted, so consider a binary search here if required.
    index = self.getLastIndex()
    while self.getDate(index) > getDate(dateNumber):
      index -= 1
    self.__list.insert(index+1, dateNumber)

  def delete(self, index):
    del(self.__list[index])


  def clear(self):
    self.__list[:] = []

  def getPair(self, index):
    if not self.isValidIndex(index):
      return None
    return self.__list[index]

  def getDate(self, index):
    if not self.isValidIndex(index):
      return None
    return getDate(self.getPair(index))

  def getFirstNumber(self):
    if not self.isValidIndex(0):
      return None
    return self.getNumber(0)

  def getFirstDate(self):
    if not self.isValidIndex(0):
      return None
    return self.getDate(0)

  def getLastNumber(self):
    if self.isEmpty():
      return None
    return self.getNumber(self.getLastIndex())

  def getLastDate(self):
    if self.isEmpty():
      return None
    return self.getDate(self.getLastIndex())

  def isInRange(self, date):
    if self.isEmpty():
      return False
    return date >= self.getFirstDate() and date <= self.getLastDate()

  def getIndexBelow(self, date):
    if self.isEmpty():
      return None

    index = 0
    
    # Scan upwards in list until end or passed the wanted date.
    while self.isValidIndex(index) and self.getDate(index) <= date:
      index += 1
    index -= 1

    if not self.isValidIndex(index):
      return None

    return index


  def getFlankingIndices(self, date):
    if not self.isInRange(date):
      return (None, None)

    lowerIndex = self.getIndexBelow(date);
    if self.getDate(lowerIndex) == date:
      return (lowerIndex, lowerIndex)
    upperIndex = lowerIndex + 1;
    return (lowerIndex, upperIndex)



  def getNumber(self, index):
    if not self.isValidIndex(index):
      return None
    return getNumber(self.getPair(index))

  def getSize(self):
    return len(self.__list)

  def isEmpty(self):
    return self.getSize() == 0

  def getLastIndex(self):
    if self.isEmpty():
      return None
    return self.getSize() - 1

  def isValidIndex(self, index):
    return not self.isEmpty() and index >= 0 and index <= self.getLastIndex()

  def __gettitem__(self, index):
    return self.getPair(index)

  def __iter__(self):
    return iter(self.__list)





class NumberSequence(object):
  """A NumberSequence is an object that translates dates to floating point
numbers. Subclasses provide various ways of doing this translations."""

  def getNumber(self, date):
    """Returns the number associated with the given date. Implemented by subclasses."""
    return None



class FixedNumber(NumberSequence):
  """The FixedNumber NumberSequence returns the same number for all dates."""

  def __init__(self, number):
    self.__number = number

  def getNumber(self, date):
    """Returns the stored number."""
    return self.__number



class StepNumber(NumberSequence):
  """The StepNumber NumberSequence contains a sequence of fixed numbers, each
  number belonging to a range of dates."""

  def __init__(self, dateNumberList):
    """The dateNumberList should be a list of two-element tuples where the
    first element of each tuple is a date and the second element is a number."""
    if isinstance(dateNumberList, DateNumberList):
      self.__dateNumberList = dateNumberList
    else:
      self.__dateNumberList = DateNumberList(sorted(dateNumberList, key = lambda entry: entry[0]))

  def getNumber(self, date):
    if len(self.__dateNumberList) == 0:
      return None
    lastNumber = self.__dateNumberList[0][1]
    for listDate,number in self.__dateNumberList:
      if listDate > date:
        return lastNumber
      else:
        lastNumber = number
    return lastNumber



class LinearInterpolation(NumberSequence):
  """The LinearInterpolation NumberSequence contains a sequence of fixed numbers, each
  number associated with a particular dates. Queries for intermediate dates will return
  values linearly interpolated between the two neighboring values."""

  def __init__(self, dateNumberList):
    """The dateNumberList should be a list of two-element tuples wihere the
    first element of each tuple is a date and the second element is a number."""
    self.__dateNumberList = DateNumberList(sorted(dateNumberList, key = lambda entry: entry[0]))

  def getNumber(self, date):
    if not self.__dateNumberList.isInRange(date):
      return None

    lowerIndex, upperIndex = self.__dateNumberList.getFlankingIndices(date);
    if lowerIndex == None or upperIndex == None:
      return None

    if (lowerIndex == upperIndex):
      return self.__dateNumberList.getNumber(lowerIndex)

    lowerDate = self.__dateNumberList.getDate(lowerIndex);
    upperDate = self.__dateNumberList.getDate(upperIndex);

    totalTime = (upperDate - lowerDate).total_seconds()
    partTime = (date - lowerDate).total_seconds()
    progress = float(partTime) / float(totalTime)

    lowerNumber = self.__dateNumberList.getNumber(lowerIndex)
    upperNumber = self.__dateNumberList.getNumber(upperIndex)
    numberDiff = upperNumber - lowerNumber

    return lowerNumber + numberDiff*progress


  def getDateNumberList(self):
    return self.__dateNumberList

