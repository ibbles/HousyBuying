#!/usr/bin/python

from Accounts import Account
from CurveFrame import CurveFrame
from GraphFrame import GraphFrame
from NumberSequences import DateNumberList

from datetime import date

from NumberSequences import LinearInterpolation
from Interest import Interest

import wx

class AccountWidget(wx.Panel):

  def __init__(self, account, parent, frame):
    wx.Panel.__init__(self, parent, -1)
    self.account = account
    self.frame = frame
    box = wx.StaticBox(self, -1, account.getName())
    sizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
    self.startAmountText = wx.TextCtrl(self, -1, value=str(int(account.getBalance())), style=wx.TE_PROCESS_ENTER)
    krText = wx.StaticText(self, -1, label="kr")
    self.interest = wx.Button(self, -1, label="Interest")
    self.saving = wx.Button(self, -1, label="Saving")
    self.balance = wx.Button(self, -1, label="Balance")
    self.balance.Disable()
    self.endBalance = wx.StaticText(self, -1, label="Final balance: {:<16}".format(0))
    self.totalInterest = wx.StaticText(self, -1, label="Total interest: {:<16}".format(0))
    self.totalSavings = wx.StaticText(self, -1, label="Total savings: {:<16}".format(0))

    sizer.Add(self.startAmountText)
    sizer.Add(krText)
    sizer.Add(self.interest)
    sizer.Add(self.saving)
    sizer.Add(self.balance)

    statsBox = wx.StaticBox(self, -1, "")
    statsSizer = wx.StaticBoxSizer(statsBox, wx.VERTICAL)
    statsSizer.Add(self.endBalance)
    statsSizer.Add(self.totalInterest)
    statsSizer.Add(self.totalSavings)
    sizer.Add(statsSizer)
    
    self.SetSizerAndFit(sizer)

    self.Bind(wx.EVT_BUTTON, self.interestClicked, self.interest)
    self.Bind(wx.EVT_BUTTON, self.savingClicked, self.saving)
    self.Bind(wx.EVT_BUTTON, self.balanceClicked, self.balance)

    dateNumberList = account.getDateInterestList().getInterestCalculator().getDateNumberList()
    self.interestFrame = CurveFrame(dateNumberList, 5.0, 10.0, 0.1, "%", "Interest for {}".format(account.getName()))
    dateNumberList = account.getSavingPlan()
    self.savingFrame = CurveFrame(dateNumberList, 0.0, 1000.0, 10.0, " kr", "Saving for {}".format(account.getName()))
    self.balanceFrame = GraphFrame("Balance for {}".format(account.getName()))


  def enableBalance(self):
    self.balance.Enable()


  def interestClicked(self, event):
    print("Interest clicked")
    if self.interestFrame.IsShown():
      self.interestFrame.Hide()
    else:
      self.frame.gatherAndApplyUserSettings()
      self.interestFrame.Show()


  def savingClicked(self, event):
    print("Saving clicked")
    if (self.savingFrame.IsShown()):
      self.savingFrame.Hide()
    else:
      self.frame.gatherAndApplyUserSettings()
      self.savingFrame.Show()


  def balanceClicked(self, event):
    print("Balance clicked")
    if self.balanceFrame.IsShown():
      self.balanceFrame.Hide()
    else:
      self.balanceFrame.Show()


  def setAccountBalanceFromUser(self):
    try:
      startBalance = int(self.startAmountText.GetValue())
      self.account.setBalance(startBalance)

    except ValueError:
      message = "The entered amount '{}' is not a valid amount.".format(self.startAmountText.GetValue())
      print(message)
      wx.MessageBox(message, 'Error', wx.OK | wx.ICON_ERROR)


  def setBalances(self, dates, balances):
    self.balanceFrame.setGraph(dates, balances)
    if len(balances) > 0:
      self.endBalance.SetLabel("Final balance: {:<16}".format(int(round(balances[len(balances)-1]))))
    else:
      self.endBalance.SetLabel("Final balance: {:<16}".format(0))


  def setTotalInterest(self, totalInterest):
    self.totalInterest.SetLabel("Total interest: {:<16}".format(int(round(totalInterest))))


  def setTotalSavings(self, totalSavings):
    self.totalSavings.SetLabel("Total savings: {:<16}".format(int(round(totalSavings))))


  def shutdown(self):
    self.interestFrame.Destroy()
    self.interestFrame = None
    self.savingFrame.Destroy()
    self.savingFrame = None
    self.balanceFrame.Destroy()
    self.balanceFrame = None






if __name__ == "__main__":
  app = wx.PySimpleApp()
  app.frame = AccountFrame()
  app.frame.Show()
  app.MainLoop()


#class simpleapp_wx(wx.Frame):
#    def __init__(self,parent,id,title):
#        wx.Frame.__init__(self,parent,id,title)
#        self.parent = parent
#        self.initialize()
#
#    def initialize(self):
#        sizer = wx.GridBagSizer()
#        self.SetSizerAndFit(sizer)
#        self.Show(True)
#
#if __name__ == "__main__":
#    app = wx.App()
#    frame = simpleapp_wx(None,-1,'my application')
#    app.MainLoop()
