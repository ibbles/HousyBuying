
class Account(tuple):
  def __init__(self, balance=0.0, storedInterest=0.0, interest=None):
    if balance == None:
      balance = 0.0
    if storedInterest == None:
      storedInterest = 0.0
    if interestRate == None:
      interestRate = Interest(InterestRate(LinearInterpolation(DateNumberList([]))))
    self.__balance = balance
    self.__storedInterest = storedInterest
    self.__interestRate = interestRate


  def getBalance(self):
    return self.__balance

  def getStoredInterest(self):
    return self.__storedInterest

  def deposit(self, amount):
    self.__balance += amount

  def withdraw(self, amount):
    self.__balance -= amount

  def applyInterest(self, date):

    return Account(self.__balance, self.__storedInterest+interest.calculateInterest(self.__balance, date, timeFraction))

  def collectInterest(self):
    self.__balance += self.__storedInterest
    self.__storedInterest = 0.0