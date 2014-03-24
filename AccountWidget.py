#!/usr/bin/python

from Accounts import Account
from CurveFrame import CurveFrame
from NumberSequences import DateNumberList


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
    text_field = wx.TextCtrl(self, -1, value="2014", style=wx.TE_PROCESS_ENTER)
    krText = wx.StaticText(self, -1, label="kr")
    interest = wx.Button(self, -1, label="Interest")
    balance = wx.Button(self, -1, label="Balance")
    sizer.Add(text_field)
    sizer.Add(krText)
    sizer.Add(interest)
    sizer.Add(balance)
    self.SetSizerAndFit(sizer)

    self.Bind(wx.EVT_BUTTON, self.interestClicked, interest)
    self.Bind(wx.EVT_BUTTON, self.balanceClicked, balance)

    self.interestFrame = CurveFrame(DateNumberList([]), "Interest for {}".format(account.getName()))



  def interestClicked(self, event):
    print("Interest clicked")
    if (self.interestFrame.IsShown()):
      self.interestFrame.Hide()
    else:
      self.frame.updateYearRange(None)
      self.interestFrame.Show()

  def balanceClicked(self, event):
    print("Balance clicked")

  def shutdown(self):
    self.interestFrame.Destroy()
    self.interestFrame = None




class AccountFrame(wx.Frame):
  def __init__(self):
    wx.Frame.__init__(self, None, -1, "Accounts")
    self.panel = wx.Panel(self)
    
    self.vbox = wx.BoxSizer(wx.VERTICAL)

    self.yearRangeBoxesPanel = wx.Panel(self.panel)
    self.yearRangeBoxesSizer = wx.BoxSizer(wx.HORIZONTAL)
    self.minYearText = wx.TextCtrl(self.yearRangeBoxesPanel, -1, value="2014", style=wx.TE_PROCESS_ENTER)
    self.maxYearText = wx.TextCtrl(self.yearRangeBoxesPanel, -1, value="2015", style=wx.TE_PROCESS_ENTER)
    self.Bind(wx.EVT_TEXT_ENTER, self.updateYearRange, self.minYearText)
    self.Bind(wx.EVT_TEXT_ENTER, self.updateYearRange, self.maxYearText)
    self.yearRangeBoxesSizer.Add(self.minYearText, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
    self.yearRangeBoxesSizer.Add(self.maxYearText, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
    self.yearRangeBoxesPanel.SetSizer(self.yearRangeBoxesSizer)
    self.yearRangeBoxesSizer.Fit(self.yearRangeBoxesPanel)
    self.vbox.Add(self.yearRangeBoxesPanel)
    
    self.accounts = [];
    self.createAccount("Savings")
    self.createAccount("Loan")

    self.calculateButton = wx.Button(self.panel, -1, label='Calculate')
    self.Bind(wx.EVT_BUTTON, self.onCalculate, self.calculateButton)
    self.vbox.Add(self.calculateButton)

    self.panel.SetSizer(self.vbox)
    self.vbox.Fit(self)

    self.Bind(wx.EVT_CLOSE, self.onShutdown)


  def createAccount(self, name):
    account = Account(name)
    accountWidget = AccountWidget(account, self.panel, self)
    self.vbox.Add(accountWidget)
    self.accounts.append(type('AccountWidgetPair', (object,), {'account' : account, 'widget' : accountWidget})())


  def updateYearRange(self, event):
    try:
      userFirstDate = date(int(self.minYearText.GetValue()), 1, 1)
      userLastDate = date(int(self.maxYearText.GetValue()), 1, 1)
      if userFirstDate.year == userLastDate.year:
        userLastDate = date(userLastDate.year+1, 1, 1)
      if userFirstDate > userLastDate:
        userFirstDate, userLastDate = userLastDate, userFirstDate
        self.minYearText.SetValue("{}".format(userFirstDate.year))
        self.maxYearText.SetValue("{}".format(userLastDate.year))

      for account in self.accounts:
        account.widget.interestFrame.setYearRange(userFirstDate, userLastDate)
    except ValueError:
      message = "The entered year '{}' or '{}' is not a valid year.".format(self.minYearText.GetValue(), self.maxYearText.GetValue())
      print(message)
      wx.MessageBox(message, 'Error', wx.OK | wx.ICON_ERROR)


  def onCalculate(self, event):
    print("Calculate clicked")


  def onShutdown(self, event):
    for account in self.accounts:
      account.widget.shutdown()
    self.Destroy()
    event.Skip(True)



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
