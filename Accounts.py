
from Interest import Interest
from NumberSequences import DateNumberList
from NumberSequences import LinearInterpolation

import math

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
    self.name = name
    self.balance = balance
    self.storedInterest = storedInterest
    self.interestRate = interestRate
    self.saving = LinearInterpolation(DateNumberList([]))


  def reset(self):
    self.balance = 0.0
    self.storedInterest = 0.0

  def getName(self):
    return self.name

  def getBalance(self):
    return self.balance

  def setBalance(self, balance):
    self.balance = balance

  def getStoredInterest(self):
    return self.storedInterest

  def getSavingPlan(self):
    return self.saving.getDateNumberList()

  def getDateInterestList(self):
    return self.interestRate

  def deposit(self, amount):
    self.balance += amount

  def withdraw(self, amount):
    self.balance -= amount

  def applyInterest(self, date, timeFraction = None):
    interest = self.interestRate.calculateInterest(self.balance, date, timeFraction)
    self.storedInterest += interest
    return interest

  def addSaving(self, date):
    saving = self.saving.getNumber(date)
    self.balance += saving
    return saving

  def collectInterest(self):
    storedInterest = self.storedInterest
    self.storedInterest = 0.0
    self.balance += storedInterest
    return storedInterest



class Loan(Account):
  """A Loan is an account that doesn't increase it's balance due to interest or
  savings. Instead it reduces the balance of some other account.

  The two overriding methods are collectInterest and addSaving, which both call
  withdraw() on the paying account.
  """

  def __init__(self, name, payingAccount, interestRate=None, balance=0.0, storedInterest=0.0, ):
    Account.__init__(self, name, interestRate, balance, storedInterest)
    self.payingAccount = payingAccount


  def collectInterest(self):
    storedInterest = self.storedInterest
    self.storedInterest = 0.0
    # print("Loan.collectInterest. Removing {} from paying account containing {}.".format(storedInterest, self.payingAccount.getBalance()))
    self.payingAccount.withdraw(storedInterest)
    # print("  Paying account now has {} left.".format(self.payingAccount.getBalance()))

    return storedInterest


  def addSaving(self, date):
    saving = self.saving.getNumber(date)
    # Don't pay more than what remains of the loan.;
    saving = min(saving, self.getBalance())
    self.payingAccount.withdraw(saving)
    # print("Loan.addSaving for date {}. Removing {} from paying account containing {}.".format(date, saving, self.payingAccount.getBalance()))
    self.withdraw(saving)
    # print("  Paying account now has {} left.".format(self.payingAccount.getBalance()))

    return saving
