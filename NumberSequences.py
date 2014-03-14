
def getDate(dateNumber):
  return dateNumber[0]

def getNumber(dateNumber):
  return dateNumber[1]



class NumberList(object):
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

  def getPair(self, index):
    return self.__list[index]

  def getDate(self, index):
    return getDate(self.__list[index])

  def getFirstDate(self):
    return getDate(self.__list[0])

  def getLastDate(self):
    return getDate(self.__list[self.getLastIndex()])

  def getNumber(self, index):
    return getNumber(self.__list[index])

  def getSize(self):
    return len(self.__list)

  def getLastIndex(self):
    if self.getSize() == 0:
      return None
    return self.getSize() - 1



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
    if isinstance(dateNumberList, NumberList):
      self.__dateNumberList = dateNumberList
    else:
      self.__dateNumberList = NumberList(sorted(dateNumberList, key = lambda entry: entry[0]))

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
    self.__dateNumberList = sorted(dateNumberList, key = lambda entry: entry[0])

    def getNumber(self, date):
      if len(self.__dateNumberList) == 0:
        return None
      if getDate(self.dateNumberList[0]) > date:
        return getValue(self.dateNumberList[0])
