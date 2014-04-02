
from datetime import timedelta
import calendar

import sys

def log(message):
  # pass
  sys.stdout.write(message)


class StepResult(object):
  def __init__(self):
    self.dates = []
    self.balances = []
    self.addedInterests = []
    self.collectedInterests = []
    self.savings = []



class Stepper(object):
  def __init__(self):
    pass


  def stepAccounts(self, accounts, startDate, endDate, progressListener):
    results = []
    for account in accounts:
      results.append(StepResult())

    if progressListener != None:
      numYears = endDate.year - startDate.year
      if numYears > 10:
        progressListener.progressStarted(numYears)
      else:
        progressListener = None

    date = startDate
    aborted = False
    while date < endDate and not aborted:
      self.recordCurrentBalance(date, accounts, results)
      self.recordInterest(date, accounts, results)

      date += timedelta(days=1)

      if date.day == 1:
        self.recordSavings(date, accounts, results)

      if date.month == 1 and date.day == 1:
        self.collectInterests(accounts, results)
        if progressListener != None:
          currentYear = date.year - startDate.year
          aborted = progressListener.progressUpdate(currentYear)
    
    self.recordCurrentBalance(date, accounts, results)

    if progressListener != None:
      progressListener.progressDone()

    return results




  def recordCurrentBalance(self, date, accounts, results):
    for index in range(0, len(accounts)):
      account = accounts[index]
      result = results[index]

      result.dates.append(date)
      result.balances.append(account.getBalance())


  def recordInterest(self, date, accounts, results):
    if calendar.isleap(date.year):
      timeFraction = 1.0/366.0
    else:
      timeFraction = 1.0/365.0

    for index in range(0, len(accounts)):
      account = accounts[index]
      result = results[index]

      addedInterest = account.applyInterest(date, timeFraction)
      result.addedInterests.append(addedInterest)


  def recordSavings(self, date, accounts, results):
    for index in range(0, len(accounts)):
      account = accounts[index]
      result = results[index]

      saving = account.addSaving(date)
      result.savings.append(saving)

  def collectInterests(self, accounts, results):
    for index in range(0, len(accounts)):
      account = accounts[index]
      result = results[index]

      collectedInterest = account.collectInterest()
      result.collectedInterests.append(collectedInterest)