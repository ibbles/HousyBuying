#!/usr/bin/python

from Accounts import Account
from AccountWidget import AccountWidget
from AccountFrame import AccountFrame

from Stepper import Stepper

from datetime import date

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
    for account in self.accounts:
      dates, balances, adededInterests, collectedInterests = \
        stepper.stepAccount(account.account, date(self.startYear, 1, 1), date(self.endYear, 1, 1))

      account.widget.setBalances(dates, balances)

    self.mainWindow.enableBalances()


  def shutdown(self):
    self.mainWindow.shutdown();


  ##
  # Callbacks from the GUI.
  ##

  def guiYearRangeChanged(self, startYear, endYear):
    self.updateYearRange(startYear, endYear)

  def guiCreateAccountCallback(self, name):
    self.createAccount(name)

  def guiCalculate(self):
    self.calculate()

  def guiShutdown(self):
    self.shutdown()


if __name__ == '__main__':
  HouseBuying()
