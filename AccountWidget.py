#!/usr/bin/python

from Accounts import Account
from CurveFrame import CurveFrame
from NumberSequences import DateNumberList
from Stepper import Stepper

from datetime import date

from NumberSequences import LinearInterpolation
from Interest import Interest

import wx

class AccountWidget(wx.Panel):

  def __init__(self, account, parent, frame):
    wx.Panel.__init__(self, parent, -1)
    self.frame = frame
    box = wx.StaticBox(self, -1, account.getName())
    sizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
    text_field = wx.TextCtrl(self, -1, value=str(account.getBalance()), style=wx.TE_PROCESS_ENTER)
    krText = wx.StaticText(self, -1, label="kr")
    self.interest = wx.Button(self, -1, label="Interest")
    self.balance = wx.Button(self, -1, label="Balance")
    self.balance.Disable()
    sizer.Add(text_field)
    sizer.Add(krText)
    sizer.Add(self.interest)
    sizer.Add(self.balance)
    self.SetSizerAndFit(sizer)

    self.Bind(wx.EVT_BUTTON, self.interestClicked, self.interest)
    self.Bind(wx.EVT_BUTTON, self.balanceClicked, self.balance)

    dateNumberList = account.getDateInterestList().getInterestCalculator().getDateNumberList()
    self.interestFrame = CurveFrame(dateNumberList, "Interest for {}".format(account.getName()))


  def enableBalance(self):
    self.balance.Enable()


  def interestClicked(self, event):
    print("Interest clicked")
    if (self.interestFrame.IsShown()):
      self.interestFrame.Hide()
    else:
      self.frame.gatherAndApplyUserSettings()
      self.interestFrame.Show()


  def balanceClicked(self, event):
    print("Balance clicked")


  def shutdown(self):
    self.interestFrame.Destroy()
    self.interestFrame = None






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
