from operator import itemgetter
from NumberSequences import FixedNumber


class Interest(object):

  def __init__(self, interestRate):
    if isinstance(interestRate, float) or isinstance(interestRate, int):
      self.__interestRate = FixedNumber(float(interestRate))
    else:
      self.__interestRate = interestRate


  def getInterestCalculator(self):
    return self.__interestRate;


  def calculateInterest(self, initialAmount, date, timeFraction=None):
    if timeFraction == None:
      timeFraction = 1.0/12.0 # Default to one month interest.
    
    currentRate = self.__interestRate.getNumber(date)
    if currentRate == None:
      return None

    interestRate = currentRate / 100.0
    return initialAmount * interestRate * timeFraction;


  def save(self, node):
    node['rate'] = {}
    self.__interestRate.save(node['rate'])

  def load(self, node):
    self.__interestRate.load(node['rate'])
