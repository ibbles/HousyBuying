from datetime import date

from AccountWidget import AccountWidget

import wx

class AccountFrame(wx.Frame):
  accounts = []
  callbacks = None

  def __init__(self, callbacks, startYear, endYear):
    wx.Frame.__init__(self, None, -1, "Accounts")
    self.callbacks = callbacks
    self.panel = wx.Panel(self)
    
    self.vbox = wx.BoxSizer(wx.VERTICAL)

    self.yearRangeBoxesPanel = wx.Panel(self.panel)
    self.yearRangeBoxesSizer = wx.BoxSizer(wx.HORIZONTAL)
    self.minYearText = wx.TextCtrl(self.yearRangeBoxesPanel, -1, value=str(startYear), style=wx.TE_PROCESS_ENTER)
    self.maxYearText = wx.TextCtrl(self.yearRangeBoxesPanel, -1, value=str(endYear), style=wx.TE_PROCESS_ENTER)
    self.Bind(wx.EVT_TEXT_ENTER, self.callbackYearRangeTriggered, self.minYearText)
    self.Bind(wx.EVT_TEXT_ENTER, self.callbackYearRangeTriggered, self.maxYearText)
    self.yearRangeBoxesSizer.Add(self.minYearText, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
    self.yearRangeBoxesSizer.Add(self.maxYearText, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
    self.yearRangeBoxesPanel.SetSizer(self.yearRangeBoxesSizer)
    self.yearRangeBoxesSizer.Fit(self.yearRangeBoxesPanel)
    self.vbox.Add(self.yearRangeBoxesPanel)
    
    #self.accounts = [];
    #self.createAccount("Savings")
    # self.createAccount("Loan")

    buttonsPanel = wx.Panel(self.panel)
    buttonsSizer = wx.BoxSizer(wx.HORIZONTAL)

    self.addAccountButton = wx.Button(buttonsPanel, -1, label='Add account')
    self.Bind(wx.EVT_BUTTON, self.callbackCreateAccountTriggered, self.addAccountButton)
    buttonsSizer.Add(self.addAccountButton)

    self.calculateButton = wx.Button(buttonsPanel, -1, label='Calculate')
    self.Bind(wx.EVT_BUTTON, self.callbackCalculateTriggered, self.calculateButton)
    buttonsSizer.Add(self.calculateButton)

    buttonsPanel.SetSizer(buttonsSizer)
    buttonsSizer.Fit(buttonsPanel)
    self.vbox.Add(buttonsPanel)

    self.panel.SetSizer(self.vbox)
    self.vbox.Fit(self)

    self.Bind(wx.EVT_CLOSE, self.callbackShutdownTriggered)

    self.updateYearRange(startYear, endYear)



  def gatherAndApplyUserSettings(self):
    self.callbackYearRangeTriggered(None)
    for account in self.accounts:
      account.widget.setAccountBalanceFromUser()


  ##
  # GUI widget callbacks. Mostly passed on to the callbacks bundle for processing.
  # Some argument assembly may be required first.
  ##


  def callbackYearRangeTriggered(self, event):
    try:
      userFirstYear = int(self.minYearText.GetValue())
      userLastYear = int(self.maxYearText.GetValue())
      self.callbacks.guiYearRangeChanged(userFirstYear, userLastYear)

    except ValueError:
      message = "The entered year '{}' or '{}' is not a valid year.".format(self.minYearText.GetValue(), self.maxYearText.GetValue())
      print(message)
      wx.MessageBox(message, 'Error', wx.OK | wx.ICON_ERROR)


  def callbackCreateAccountTriggered(self, event):
    dialog = wx.TextEntryDialog(self, 'Account name', 'Enter account name', '')
    if dialog.ShowModal() == wx.ID_OK:
      name = dialog.GetValue()
      self.callbacks.guiCreateAccountCallback(name)
    

  def callbackCalculateTriggered(self, event):
    self.callbacks.guiCalculate()


  def callbackShutdownTriggered(self, event):
    self.callbacks.guiShutdown()
    event.Skip(True)



  ##
  # Worker methods called by some master object. Many of the self.callbacks.guiXXX()
  # calls in the callbackXXXTriggered() methods end up in one of these.
  ##


  def updateYearRange(self, startYear, endYear):
    self.minYearText.SetValue("{}".format(startYear))
    self.maxYearText.SetValue("{}".format(endYear))

    self.startDate = date(startYear, 1, 1)
    self.endDate = date(endYear, 1, 1)

    for account in self.accounts:
      account.widget.interestFrame.setYearRange(self.startDate, self.endDate)
      account.widget.savingFrame.setYearRange(self.startDate, self.endDate)


  def createAccountWidget(self, account):
    accountWidget = AccountWidget(account, self.panel, self)
    self.vbox.Add(accountWidget)
    self.accounts.append(type('AccountWidgetPair', (object,), {'account' : account, 'widget' : accountWidget})())

    self.vbox.Fit(self)

    return accountWidget


  def enableBalances(self):
    for account in self.accounts:
      account.widget.enableBalance()


  def updateBalance(self, accountIndex, dates, balances):
    widget = self.accounts[index].widget
    widget.setBalances(dates, balances)

  def updateBalances(self, dates, balancesList):
    assert len(balancesList) == len(self.accounts)

    for i in range(0, len(self.accounts)):
      widget = self.accounts[i].widget
      widget.setBalances(dates, balancesList[i])


  def shutdown(self):
    for account in self.accounts:
      account.widget.shutdown()
    self.Destroy()

