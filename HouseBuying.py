#!/usr/bin/python

# Imports for my own classes.
from Accounts import Account
from Accounts import Loan
from AccountWidget import AccountWidget
from AccountFrame import AccountFrame
from Stepper import Stepper

# System imports.
from datetime import date
import json
import math
import sys
import wx



class AccountHandle(object):
  """
  A bridge between the GUI representation of an account and the data
  representation of the same account.
  """

  account = None
  """The data representation. An instance of Account."""

  widget = None
  """The GUI representation. An instance of AccountWidget."""


  def __init__(self, account, widget):
    self.account = account
    self.widget = widget
  


class HouseBuying(object):
  """
  The main driver of the application. Creates and shows the GUI, and acts as a
  hub for callbacks, distributing them over the various components of the
  system.
  """
  

  accounts = []
  """The accounts present in the system, as AccountHandle instances."""

  mainWindow = None
  """The main application window containing a set of AccountWidgets and buttons to manipulate them."""

  startYear = None
  """The year that the calculation starts. January first is assumed."""

  endYear = None
  """The year that the calculation ends. January first is assumed."""


  def __init__(self, filename):
    app = wx.PySimpleApp()

    self.startYear = 2014
    self.endYear = 2015
    self.mainWindow = AccountFrame(self, self.startYear, self.endYear)

    app.frame = self.mainWindow
    
    if filename != None:
      self.load(filename)
    
    app.frame.Show()

    if filename != None:
      self.calculate()

    app.MainLoop()


  ##
  # Worker methods
  ##

  def createAccount(self, name):
    account = Account(name, balance = 0)
    widget = self.mainWindow.createAccountWidget(account)
    self.accounts.append(AccountHandle(account, widget))


  def createLoan(self, name, payingAccountName = None):
    if len(self.accounts) == 0:
      print('Must create a regular account before any loans can be added'); # TODO: Error dialog.
      return
    if payingAccountName != None:
      for account in self.accounts:
        if account.account.getName() == payingAccountName:
          payingAccount = account.account
          break
    else:
      payingAccount = self.accounts[0].account
    loan = Loan(name, payingAccount)
    widget = self.mainWindow.createAccountWidget(loan)
    self.accounts.append(AccountHandle(loan, widget))


  def updateYearRange(self, startYear, endYear):
    if startYear == endYear:
      endYear += 1
    if startYear > endYear:
      startYear, endYear = endYear, startYear
      
    self.mainWindow.updateYearRange(startYear, endYear)
    self.startYear = startYear
    self.endYear = endYear


  def calculate(self):
    if len(self.accounts) == 0:
      return

    for account in self.accounts:
      account.account.reset()

    self.mainWindow.gatherAndApplyUserSettings()
    stepper = Stepper()
    accounts = []
    for account in self.accounts:
      accounts.append(account.account)


    results = stepper.stepAccounts(accounts, date(self.startYear, 1, 1), date(self.endYear, 1, 1), self.mainWindow)

    assert len(results) == len(self.accounts)

    minimums = []
    for index in range(0, len(results)):
      result = results[index]
      widget = self.accounts[index].widget
      widget.updateGraphs(result)

      minimums.append(min(result.balances.numbers))

      totalInterest = math.fsum(result.collectedInterests.numbers)
      totalSavings = math.fsum(result.savings.numbers)
      widget.setTotalInterest(totalInterest)
      widget.setTotalSavings(totalSavings)

    self.mainWindow.enableBalances()
    self.mainWindow.Fit()

    if min(minimums) < 0:
      wx.MessageBox("An account ran out of money. Results may not be valid.", 'Error', wx.OK | wx.ICON_ERROR)


  def save(self, filename):
    if filename == None or len(filename) == 0:
      return;

    self.mainWindow.gatherAndApplyUserSettings()

    print("Saving to file '{}'.".format(filename))
    rootNode = {}
    rootNode['startYear'] = self.startYear
    rootNode['endYear'] = self.endYear
    rootNode['accounts'] = []
    for accountHandle in self.accounts:
      account = accountHandle.account
      accountNode = {}
      account.save(accountNode)
      rootNode['accounts'].append(accountNode)

    with open(filename, 'w') as file:
      json.dump(rootNode, file, indent=2, sort_keys=True)



  def load(self, filename):
    if filename == None or len(filename) == 0:
      return;

    print("Loading from file '{}'.".format(filename))
    with open(filename, 'r') as file:
      rootNode = json.load(file)

    for accountNode in rootNode['accounts']:
      name = accountNode['name']
      if 'payingAccount' in accountNode:
        self.createLoan(name, accountNode['payingAccount'])
      else:
        self.createAccount(name)
      self.accounts[-1].account.load(accountNode)
      self.accounts[-1].widget.startAmountText.SetValue("{}".format(int(self.accounts[-1].account.getBalance())))
      self.accounts[-1].widget.interestFrame.copyNumbersToPlotData()
      self.accounts[-1].widget.savingFrame.copyNumbersToPlotData()

    self.updateYearRange(rootNode['startYear'], rootNode['endYear'])



  def shutdown(self):
    self.mainWindow.shutdown();


  ##
  # Callbacks from the GUI.
  ##

  def guiYearRangeChanged(self, startYear, endYear):
    self.updateYearRange(startYear, endYear)

  def guiCreateAccountCallback(self, name):
    self.createAccount(name)

  def guiCreateLoanCallback(self, name):
    self.createLoan(name)

  def guiCalculate(self):
    self.calculate()

  def guiShutdown(self):
    self.shutdown()

  def guiSave(self, filename):
    self.save(filename)

  def guiLoad(self, filename):
    self.load(filename)




if __name__ == '__main__':
  if len(sys.argv) == 2:
    loadFile = sys.argv[1]
  else:
    loadFile = None

  HouseBuying(loadFile)
