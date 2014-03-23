from operator import itemgetter
from NumberSequences import FixedNumber


class Interest(tuple):

  def __init__(self, interestRate):
    if isinstance(interestRate, float) or isinstance(interestRate, int):
      self.__interestRate = InterestRate(FixedNumber(float(interestRate)))
    else:
      self.__interestRate = interestRate


  def calculateInterest(self, initialAmount, date, timeFraction=None):
    if timeFraction == None:
      timeFraction = 1.0/12.0 # Default to one month interest.
    
    interestRate = self.__interestRate.getNumber(date) / 100
    return initialAmount * interestRate * timeFraction;


