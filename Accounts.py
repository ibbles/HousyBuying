
from Interest import Interest
from NumberSequences import DateNumberList
from NumberSequences import LinearInterpolation

class Account(object):
  def __init__(self, name, interestRate=None, balance=0.0, storedInterest=0.0):
    if balance == None:
      balance = 0.0
    if storedInterest == None:
      storedInterest = 0.0
    if interestRate == None:
      dateToInterestTable = DateNumberList([])
      linearInterpolation = LinearInterpolation(dateToInterestTable)
      interestRate = Interest(linearInterpolation)
    self.__name = name
    self.__balance = balance
    self.__storedInterest = storedInterest
    self.__interestRate = interestRate
    self.__saving = DateNumberList([])


  def reset(self):
    self.__balance = 0.0
    self.__storedInterest = 0.0

  def getName(self):
    return self.__name

  def getBalance(self):
    return self.__balance

  def setBalance(self, balance):
    self.__balance = balance

  def getStoredInterest(self):
    return self.__storedInterest

  def getSaving(self):
    return self.__saving

  def getDateInterestList(self):
    return self.__interestRate

  def deposit(self, amount):
    self.__balance += amount

  def withdraw(self, amount):
    self.__balance -= amount

  def applyInterest(self, date, timeFraction = None):
    interest = self.__interestRate.calculateInterest(self.__balance, date, timeFraction)
    self.__storedInterest += interest
    return interest

  def collectInterest(self):
    storedInterest = self.__storedInterest
    self.__storedInterest = 0.0
    self.__balance += storedInterest
    return storedInterest