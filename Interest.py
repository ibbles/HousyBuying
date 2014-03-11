from operator import itemgetter
from NumberSequences import FixedNumber

class InterestRate(tuple):
  __slots__ = []
  def __new__(self, numberSequence):
    return tuple.__new__(self, (numberSequence,))

  __numberSequence = property(itemgetter(0))

  def getInterestRate(self, date):
    return self.__numberSequence.getNumber(date)




class Interest(tuple):
  """Interest objects calculates interest at some point in time based on the
  amount, a time fraction, and an InterestRate."""
  __slots__ = []
  def __new__(self, interestRate):
    if isinstance(interestRate, float) or isinstance(interestRate, int):
      return tuple.__new__(self, (InterestRate(FixedNumber(float(interestRate))),))
    else:
      return tuple.__new__(self, (interestRate,))


  __interestRate = property(itemgetter(0))


  def calculateInterest(self, initialAmount, date, timeFraction):
    if timeFraction == None:
      timeFraction = 1.0
    
    return self.__interestRate.getInterestRate(date)/100.0 * timeFraction * initialAmount;


