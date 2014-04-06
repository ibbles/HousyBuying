#!/usr/bin/python

from Accounts import Account
from CurveFrame import CurveFrame
from GraphFrame import GraphFrame
from NumberSequences import DateNumberList

from datetime import date
from datetime import timedelta

from NumberSequences import LinearInterpolation
from Interest import Interest

import wx



class CurvePopupMenu(wx.Menu):
  def __init__(self, curveFrame):
    wx.Menu.__init__(self)
    self.curveFrame = curveFrame

    setXmaxItem = wx.MenuItem(self, wx.NewId(), 'Change range')
    self.AppendItem(setXmaxItem)
    self.Bind(wx.EVT_MENU, self.onXmax, setXmaxItem)


  def onXmax(self, event):
    dialog = wx.TextEntryDialog(self.curveFrame, 'New max', 'Enter new max', '')
    if dialog.ShowModal() == wx.ID_OK:
      try:
        newMax = int(dialog.GetValue())
        self.curveFrame.maxValue = newMax
        self.curveFrame.drawNumbers()
      except:
        pass


class PlotPopupMenu(wx.Menu):
  widget = None

  def __init__(self, widget):
    wx.Menu.__init__(self)
    self.widget = widget

    plotBalanceItem = wx.MenuItem(self, wx.NewId(), 'Plot balance')
    self.AppendItem(plotBalanceItem)
    self.Bind(wx.EVT_MENU, self.onPlotBalance, plotBalanceItem)

    plotMonthlyItem = wx.MenuItem(self, wx.NewId(), 'Plot monthly')
    self.AppendItem(plotMonthlyItem)
    self.Bind(wx.EVT_MENU, self.onPlotMonthly, plotMonthlyItem)


  def onPlotBalance(self, event):
    self.widget.balanceClicked(None)


  def onPlotMonthly(self, event):
    self.widget.plotMontly(None)


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
    self.plotList = wx.Button(self, -1, label="Plot")
    self.plotList.Disable()
    self.endBalance = wx.StaticText(self, -1,    label="Final balance:  {:>16}   ".format(0))
    self.totalInterest = wx.StaticText(self, -1, label="Total interest: {:>16}   ".format(0))
    self.totalSavings = wx.StaticText(self, -1,  label="Total savings:  {:>16}   ".format(0))

    self.endBalance.SetForegroundColour((200, 0, 0))
    self.totalInterest.SetForegroundColour((0, 200, 0))
    self.totalSavings.SetForegroundColour((0,0, 255))

    statsFont = self.createStatisticsFont()
    self.endBalance.SetFont(statsFont);
    self.totalInterest.SetFont(statsFont);
    self.totalSavings.SetFont(statsFont);

    self.interest.Bind(wx.EVT_CONTEXT_MENU, self.onShowInputPopup)
    self.saving.Bind(wx.EVT_CONTEXT_MENU, self.onShowInputPopup)
    self.plotList.Bind(wx.EVT_CONTEXT_MENU, self.plotListClicked)

    sizer.Add(self.startAmountText)
    sizer.Add(krText)
    sizer.Add(self.interest)
    sizer.Add(self.saving)
    sizer.Add(self.plotList)

    statsBox = wx.StaticBox(self, -1, "")
    statsSizer = wx.StaticBoxSizer(statsBox, wx.VERTICAL)
    statsSizer.Add(self.endBalance)
    statsSizer.Add(self.totalInterest)
    statsSizer.Add(self.totalSavings)
    sizer.Add(statsSizer)
    
    self.SetSizerAndFit(sizer)

    self.Bind(wx.EVT_BUTTON, self.interestClicked, self.interest)
    self.Bind(wx.EVT_BUTTON, self.savingClicked, self.saving)
    self.Bind(wx.EVT_BUTTON, self.plotListClicked, self.plotList)

    dateNumberList = account.getDateInterestList().getInterestCalculator().getDateNumberList()
    self.interestFrame = CurveFrame(dateNumberList, 5.0, 10.0, "%", "Interest for {}".format(account.getName()))
    dateNumberList = account.getSavingPlan()
    self.savingFrame = CurveFrame(dateNumberList, 0.0, 1000.0, " kr", "Saving for {}".format(account.getName()))
    self.balanceFrame = GraphFrame("Balance for {}".format(account.getName()))
    self.monthlyFrame = GraphFrame("Monthly for {}".format(account.getName()))


  def createStatisticsFont(self):
    currentFont = self.endBalance.GetFont()
    return wx.Font(currentFont.GetPointSize(), wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)


  def onShowInputPopup(self, event):
    source = event.GetEventObject()
    if id(source) == id(self.interest):
      curveFrame = self.interestFrame
    elif id(source) == id(self.saving):
      curveFrame = self.savingFrame

    pos = event.GetPosition();
    pos = self.interest.ScreenToClient(pos)
    menu = CurvePopupMenu(curveFrame)
    self.interest.PopupMenu(menu, pos)
    menu.Destroy()

  def enableBalance(self):
    self.plotList.Enable()


  def plotListClicked(self, event):
    pos = wx.GetMousePosition()
    pos = self.plotList.ScreenToClient(pos)
    menu = PlotPopupMenu(self)
    self.plotList.PopupMenu(menu, pos)
    menu.Destroy();


  def interestClicked(self, event):
    if self.interestFrame.IsShown():
      self.interestFrame.Hide()
    else:
      self.frame.gatherAndApplyUserSettings()
      self.interestFrame.Show()


  def savingClicked(self, event):
    if (self.savingFrame.IsShown()):
      self.savingFrame.Hide()
    else:
      self.frame.gatherAndApplyUserSettings()
      self.savingFrame.Show()


  def balanceClicked(self, event):
    if self.balanceFrame.IsShown():
      self.balanceFrame.Hide()
    else:
      self.balanceFrame.Show()


  def plotMontly(self, event):
    if self.monthlyFrame.IsShown():
      self.monthlyFrame.Hide()
    else:
      self.monthlyFrame.Show()



  def setAccountBalanceFromUser(self):
    try:
      startBalance = int(self.startAmountText.GetValue())
      self.account.setBalance(startBalance)

    except ValueError:
      message = "The entered amount '{}' is not a valid amount.".format(self.startAmountText.GetValue())
      print(message)
      wx.MessageBox(message, 'Error', wx.OK | wx.ICON_ERROR)






  def updateGraphs(self, results):
    self.updateBalanceGraph(results)
    self.updateMonthlyGraph(results)


  def updateBalanceGraph(self, results):
    balanceDates = results.balances.dates
    balances = results.balances.numbers
    accInterestDates = results.accumulatedIterests.dates
    accInterests = results.accumulatedIterests.numbers
    accSavingsDates = results.accumulatedSavings.dates
    accSavings = results.accumulatedSavings.numbers

    colors = ['r', 'g', 'b']

    dates = [balanceDates, accInterestDates, accSavingsDates]
    values = [balances, accInterests, accSavings]
    self.balanceFrame.setGraphs(dates, values, colors)
    if len(balances) > 0:
      self.endBalance.SetLabel("Final balance:  {:>16}   ".format(int(round(balances[len(balances)-1]))))
    else:
      self.endBalance.SetLabel("Final balance:  {:>16}   ".format(0))


  def updateMonthlyGraph(self, results):
    balancesDates, balancesValues = self.updateMonthlyBalance(results.balances)
    interestsDates, interestsValues = self.updateMontlyInterests(results.addedInterests)
    savingsDates, savingsValues = self.updateMontlySavings(results.savings);
    self.monthlyFrame.setGraphs(
      [balancesDates,  interestsDates,  savingsDates],
      [balancesValues, interestsValues, savingsValues],
      ['r', 'g', 'b'])


  def updateMonthlyBalance(self, balances):
    balancesDates = []
    balancesValues = []
    currentDate = balances.dates[0]
    currentValue = balances.numbers[0]
    for i in range(1, len(balances.dates)):
      if currentDate.month != balances.dates[i].month:
        balancesDates.append(date(currentDate.year, currentDate.month, 1))
        balancesValues.append(balances.numbers[i] - currentValue)
        currentDate = balances.dates[i]
        currentValue = balances.numbers[i]

    return balancesDates, balancesValues



  def updateMontlyInterests(self, interests):
    interestsDates = []
    interestsValues = []
    currentDate = interests.dates[0]
    currentValue = 0.0
    for i in range(0, len(interests.dates)):
      if currentDate.month == interests.dates[i].month:
        currentValue += interests.numbers[i]
      else:
        interestsDates.append(currentDate)
        interestsValues.append(currentValue)
        currentDate = interests.dates[i]
        currentValue = interests.numbers[i]


    return interestsDates, interestsValues


  def updateMontlySavings(self, savings):
    savingsDates = []
    savingsValues = []
    currentDate = savings.dates[0]
    currentValue = 0.0
    for i in range(0, len(savings.dates)):
      if currentDate.month == savings.dates[i].month:
        currentValue += savings.numbers[i]
      else:
        savingsDates.append(currentDate)
        savingsValues.append(currentValue)
        currentDate = savings.dates[i]
        currentValue = savings.numbers[i]


    return savingsDates, savingsValues



  def setTotalInterest(self, totalInterest):
    self.totalInterest.SetLabel("Total interest: {:>16}   ".format(int(round(totalInterest))))


  def setTotalSavings(self, totalSavings):
    self.totalSavings.SetLabel("Total savings:  {:>16}   ".format(int(round(totalSavings))))


  def shutdown(self):
    self.interestFrame.Destroy()
    self.interestFrame = None
    self.savingFrame.Destroy()
    self.savingFrame = None
    self.balanceFrame.Destroy()
    self.balanceFrame = None
    self.monthlyFrame.Destroy()
    self.monthlyFrame = None





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
