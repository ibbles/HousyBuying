
from Interest import Interest
from NumberSequences import DateNumberList
from NumberSequences import LinearInterpolation

import math

class Account(object):
  """
  An Account represents an amount of money along with ways of calculating
  interest and savings. The basic Account represents a normal savings account,
  and the subclass Loan represents money owed to the bank.
  """

  name = ''
  balance = 0.0
  storedInterest = 0.0

  interestRate = None
  """
  An instance of the Interest class. On every interest tick the Account will
  query this object for the current interest rate.
  """

  saving = None
  """
  An instance of a subclass of NumberSequence. On every saving tick the Account will
  query this object for the current amount to be added to the account.
  """

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

  def isLoan(self):
    return False


  def save(self, node):
    node['name'] = self.name
    node['balance'] = self.balance
    node['interestRate']  = {}
    self.interestRate.save(node['interestRate'])
    node['saving'] = {}
    self.saving.save(node['saving'])


  def load(self, node):
    # Don't need to load name here. Had to be done in order to create the account.
    self.balance = node['balance']
    self.interestRate.load(node['interestRate'])
    self.saving.load(node['saving'])


class Loan(Account):
  """
  A Loan is an account that doesn't increase it's balance due to interest or
  savings. Instead it reduces the balance of some other account.

  The two overriding methods are collectInterest and addSaving, which both call
  withdraw() on the paying account.
  """

  payingAccount = None
  """The Account from which savings and interest shold be withdrawn."""

  def __init__(self, name, payingAccount, interestRate=None, balance=0.0, storedInterest=0.0, ):
    Account.__init__(self, name, interestRate, balance, storedInterest)
    self.payingAccount = payingAccount


  def collectInterest(self):
    storedInterest = self.storedInterest
    self.storedInterest = 0.0
    self.payingAccount.withdraw(storedInterest)

    return storedInterest


  def addSaving(self, date):
    saving = self.saving.getNumber(date)
    # Don't pay more than what remains of the loan.
    saving = min(saving, self.getBalance())
    self.payingAccount.withdraw(saving)
    self.withdraw(saving)

    return saving


  def isLoan(self):
    return True

  def save(self, node):
    Account.save(self, node)
    node['payingAccount'] = self.payingAccount.getName()
