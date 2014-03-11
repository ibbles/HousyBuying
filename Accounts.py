from operator import itemgetter

class Account(tuple):
  __slots__ = []
  def __new__(self, balance=0.0, storedInterest=0.0):
    if storedInterest == None:
      storedInterest = 0.0
    return tuple.__new__(self, (balance,storedInterest))

  __balance = property(itemgetter(0))
  __storedInterest = property(itemgetter(1))

  def getBalance(self):
    return self.__balance

  def getStoredInterest(self):
    return self.__storedInterest

  def deposit(self, amount):
    return Account(self.__balance+amount, self.__storedInterest)

  def withdraw(self, amount):
    return Account(self.__balance-amount, self.__storedInterest)

  def applyInterest(self, interest, date, timeFraction):
    return Account(self.__balance, self.__storedInterest+interest.calculateInterest(self.__balance, date, timeFraction))

  def collectInterest(self):
    return Account(self.__balance+self.__storedInterest, 0.0)