
from Interest import Interest
from NumberSequences import DateNumberList
from NumberSequences import LinearInterpolation

class Account(tuple):
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


  def getName(self):
    return self.__name

  def getBalance(self):
    return self.__balance

  def getStoredInterest(self):
    return self.__storedInterest

  def getDateInterestList(self):
    return self.__interestRate

  def deposit(self, amount):
    self.__balance += amount

  def withdraw(self, amount):
    self.__balance -= amount

  def applyInterest(self, date):
    self.__storedInterest += interest.calculateInterest(self.__balance, date)

  def collectInterest(self):
    self.__balance += self.__storedInterest
    self.__storedInterest = 0.0