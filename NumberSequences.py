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
    self.__dateNumberList = sorted(dateNumberList, key = lambda entry: entry[0])

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