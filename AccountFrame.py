from datetime import date

from AccountWidget import AccountWidget

import os.path
import wx

class AccountFrame(wx.Frame):
  """
  Main window of the application. Contains two text fields for entering the
  year range and a list of AccountWidgets.
  """

  accounts = []
  """List of {account : Account, widget : AccountWidget} objects."""

  callbacks = None
  """
  The application that the window is part of. Actions triggered by the user
  will be forwarded to the application via one of the callback mewthods.
  """

  def __init__(self, callbacks, startYear, endYear):
    wx.Frame.__init__(self, None, -1, "Accounts")
    self.callbacks = callbacks
    self.createGui(startYear, endYear)
    self.updateYearRange(startYear, endYear)
    self.Bind(wx.EVT_CLOSE, self.callbackShutdownTriggered)


  def createGui(self, startYear, endYear):
    self.mainPanel = wx.Panel(self)
    self.mainPanelContents = wx.BoxSizer(wx.VERTICAL)
    self.createMenu()
    self.createYearRange(startYear, endYear)
    self.createButtons()    
    self.mainPanel.SetSizer(self.mainPanelContents)
    self.mainPanelContents.Fit(self)


  def createMenu(self):
    self.menuBar = wx.MenuBar()
    self.fileMenu = wx.Menu()
    self.saveItem = self.fileMenu.Append(wx.ID_SAVE, '&Save')
    self.Bind(wx.EVT_MENU, self.callbackSaveTriggered, self.saveItem)

    # Disabling load for now since it misbehaves when there are accounts present already.
    #self.loanItem = self.fileMenu.Append(wx.ID_OPEN, '&Open')
    #self.Bind(wx.EVT_MENU, self.callbackLoadTriggered, self.loanItem)

    self.menuBar.Append(self.fileMenu, '&File')
    self.SetMenuBar(self.menuBar)


  def createYearRange(self, startYear, endYear):
    yearRangeBoxesPanel = wx.Panel(self.mainPanel)
    yearRangeBoxesSizer = wx.BoxSizer(wx.HORIZONTAL)
    self.minYearText = wx.TextCtrl(yearRangeBoxesPanel, -1, value=str(startYear), style=wx.TE_PROCESS_ENTER)
    self.maxYearText = wx.TextCtrl(yearRangeBoxesPanel, -1, value=str(endYear), style=wx.TE_PROCESS_ENTER)
    self.Bind(wx.EVT_TEXT_ENTER, self.callbackYearChanged, self.minYearText)
    self.Bind(wx.EVT_TEXT_ENTER, self.callbackYearChanged, self.maxYearText)
    yearRangeBoxesSizer.Add(self.minYearText, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
    yearRangeBoxesSizer.Add(self.maxYearText, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
    yearRangeBoxesPanel.SetSizer(yearRangeBoxesSizer)
    yearRangeBoxesSizer.Fit(yearRangeBoxesPanel)
    self.mainPanelContents.Add(yearRangeBoxesPanel)


  def createButtons(self):
    buttonsPanel = wx.Panel(self.mainPanel)
    buttonsSizer = wx.BoxSizer(wx.HORIZONTAL)

    addAccountButton = wx.Button(buttonsPanel, -1, label='Add &account')
    self.Bind(wx.EVT_BUTTON, self.callbackCreateAccountTriggered, addAccountButton)
    buttonsSizer.Add(addAccountButton)

    addLoanButton = wx.Button(buttonsPanel, 01, label='Add &loan')
    self.Bind(wx.EVT_BUTTON, self.callbackCreateLoadTriggered, addLoanButton)
    buttonsSizer.Add(addLoanButton)

    calculateButton = wx.Button(buttonsPanel, -1, label='&Calculate')
    self.Bind(wx.EVT_BUTTON, self.callbackCalculateTriggered, calculateButton)
    buttonsSizer.Add(calculateButton)

    buttonsPanel.SetSizer(buttonsSizer)
    buttonsSizer.Fit(buttonsPanel)
    self.mainPanelContents.Add(buttonsPanel)


  def gatherAndApplyUserSettings(self):
    """
    Read all the text fields and whatnot and pass them on to whatever
    underlying datastore is responsible for storing that data.
    """
    self.readYearsAndPassToMaster()
    for account in self.accounts:
      account.widget.setAccountBalanceFromUser()



  def readYearsAndPassToMaster(self):
    try:
      userFirstYear = int(self.minYearText.GetValue())
      userLastYear = int(self.maxYearText.GetValue())
      self.callbacks.guiYearRangeChanged(userFirstYear, userLastYear)

    except ValueError:
      message = "The entered year '{}' or '{}' is not a valid year.".format(self.minYearText.GetValue(), self.maxYearText.GetValue())
      print(message)
      wx.MessageBox(message, 'Error', wx.OK | wx.ICON_ERROR)



  ##
  # GUI widget callbacks. Mostly passed on to the callbacks bundle for processing.
  # Some argument assembly may be required first.
  ##



  def callbackYearChanged(self, event):
    self.readYearsAndPassToMaster()
    

  def callbackCreateAccountTriggered(self, event):
    dialog = wx.TextEntryDialog(self, 'Account name', 'Enter account name', '')
    if dialog.ShowModal() == wx.ID_OK:
      name = dialog.GetValue()
      self.callbacks.guiCreateAccountCallback(name)


  def callbackCreateLoadTriggered(self, event):
    dialog = wx.TextEntryDialog(self, 'Loan name', 'Enter loan name', '')
    if dialog.ShowModal() == wx.ID_OK:
      name = dialog.GetValue()
      self.callbacks.guiCreateLoanCallback(name)
    

  def callbackCalculateTriggered(self, event):
    self.callbacks.guiCalculate()


  def callbackShutdownTriggered(self, event):
    self.callbacks.guiShutdown()
    event.Skip(True)


  def callbackSaveTriggered(self, event):
    print("GUI wants to save")
    dialog = wx.FileDialog(self, "Select filename", "", "houseBuying.json", "*.json", wx.FD_SAVE)
    if dialog.ShowModal() != wx.ID_OK:
      return

    filenames = dialog.GetFilenames()
    if len(filenames) != 1:
      return

    filename = filenames[0]
    if (len(filename) == 0):
      return

    exists = os.path.exists(filename)
    isfile = os.path.isfile(filename)

    if exists and isfile:
      dialog = wx.MessageDialog(None, "File '{}' exists. Overwrite?".format(filename), 'Overwrite?', wx.YES_NO | wx.ICON_QUESTION)
      if dialog.ShowModal() != wx.ID_YES:
        return

    if exists and not isfile:
      return

    self.callbacks.guiSave(filename)


  def callbackLoadTriggered(self, event):
    dialog = wx.FileDialog(self, "Select filename", "", "houseBuying.json", "*.json")
    if dialog.ShowModal() != wx.ID_OK:
      return

    filenames = dialog.GetFilenames()
    if len(filenames) != 1:
      return

    filename = filenames[0]
    if len(filename) == 0:
      return

    exists = os.path.exists(filename)
    isfile = os.path.isfile(filename)

    if not exists or not isfile:
      return

    self.callbacks.guiLoad(filename)






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
    accountWidget = AccountWidget(account, self.mainPanel, self)
    self.mainPanelContents.Add(accountWidget)
    self.accounts.append(type('AccountWidgetPair', (object,), {'account' : account, 'widget' : accountWidget})())

    self.mainPanelContents.Fit(self)

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



  ##
  # Public methods for the ProgressListener interface
  ##

  def progressStarted(self, numTicks):
    self.progress = wx.ProgressDialog("Calculating", "Calculating", numTicks, style=wx.PD_APP_MODAL|wx.PD_AUTO_HIDE|wx.PD_CAN_ABORT)

  def progressUpdate(self, tick):
    cont, skip = self.progress.Update(tick)
    return not cont

  def progressDone(self):
    self.progress.Destroy()

