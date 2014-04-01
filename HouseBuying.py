#!/usr/bin/python

from Accounts import Account
from Accounts import Loan
from AccountWidget import AccountWidget
from AccountFrame import AccountFrame

from Stepper import Stepper

from datetime import date

import json
import math
import wx

class AccountHandle(object):
  account = None
  widget = None
  master = None

  def __init__(self, account, widget, master):
    self.account = account
    self.widget = widget
    self.master = master
  

class HouseBuying(object):
  

  accounts = []
  mainWindow = None
  startYear = None
  endYear = None


  def __init__(self):
    app = wx.PySimpleApp()

    self.startYear = 2014
    self.endYear = 2015
    self.mainWindow = AccountFrame(self, self.startYear, self.endYear)

    app.frame = self.mainWindow
    app.frame.Show()
    app.MainLoop()


  ##
  # Worker methods
  ##

  def createAccount(self, name):
    account = Account(name, balance = 0)
    widget = self.mainWindow.createAccountWidget(account)
    self.accounts.append(AccountHandle(account, widget, self))


  def createLoan(self, name):
    if len(self.accounts) == 0:
      print('Must create a regular account before any loans can be added'); # TODO: Error dialog.
      return
    loan = Loan(name, self.accounts[0].account, balance = 0)
    widget = self.mainWindow.createAccountWidget(loan)
    self.accounts.append(AccountHandle(loan, widget, self))


  def updateYearRange(self, startYear, endYear):
    if startYear == endYear:
      endYear += 1
    if startYear > endYear:
      startYear, endYear = endYear, startYear
      
    self.mainWindow.updateYearRange(startYear, endYear)
    self.startYear = startYear
    self.endYear = endYear


  def calculate(self):
    for account in self.accounts:
      account.account.reset()

    self.mainWindow.gatherAndApplyUserSettings()
    stepper = Stepper()
    accounts = []
    for account in self.accounts:
      accounts.append(account.account)


    results = stepper.stepAccounts(accounts, date(self.startYear, 1, 1), date(self.endYear, 1, 1))

    assert len(results) == len(self.accounts)

    minimums = []
    for index in range(0, len(results)):
      result = results[index]
      widget = self.accounts[index].widget
      widget.setBalances(result.dates, result.balances)

      minimums.append(min(result.balances))

      totalInterest = math.fsum(result.collectedInterests)
      totalSavings = math.fsum(result.savings)
      widget.setTotalInterest(totalInterest)
      widget.setTotalSavings(totalSavings)

    self.mainWindow.enableBalances()
    self.mainWindow.Fit()

    if min(minimums) < 0:
      wx.MessageBox("An account ran out of money. Results may not be valid.", 'Error', wx.OK | wx.ICON_ERROR)


  def save(self, filename):
    if filename == None or len(filename) == 0:
      return;

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


if __name__ == '__main__':
  HouseBuying()
