#!/usr/bin/python

from Accounts import Account
from CurveFrame import CurveFrame
from NumberSequences import DateNumberList


from NumberSequences import LinearInterpolation
from Interest import Interest

import wx

class AccountWidget(wx.Panel):

  def __init__(self, account, parent):
    wx.Panel.__init__(self, parent, -1)
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
    
    self.accounts = [];
    self.vbox = wx.BoxSizer(wx.VERTICAL)
    
    self.createAccount("Savings")
    self.createAccount("Loan")

    self.panel.SetSizer(self.vbox)
    self.vbox.Fit(self)

    self.Bind(wx.EVT_CLOSE, self.onShutdown)


  def createAccount(self, name):
    account = Account(name)
    accountWidget = AccountWidget(account, self.panel)
    self.vbox.Add(accountWidget)
    self.accounts.append(type('AccountWidgetPair', (object,), {'account' : account, 'widget' : accountWidget})())


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
