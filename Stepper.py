from datetime import timedelta
import datetime
import calendar

import sys

def log(message):
  # pass
  sys.stdout.write(message)

class FastDateNumberList(object):
  endIndex = 0
  dates = None
  numbers = None

  def __init__(self, numItems):
    self.dates = [datetime.date(1,1,1)] * numItems
    self.numbers = [0.0] * numItems

  def append(self, date, number):
    self.dates[self.endIndex] = date
    self.numbers[self.endIndex] = number
    self.endIndex += 1

  def appendAccumulated(self, date, number):
    self.dates[self.endIndex] = date
    self.numbers[self.endIndex] = self.numbers[self.endIndex-1] + number
    self.endIndex += 1

  def done(self):
    del self.dates[self.endIndex:]
    del self.numbers[self.endIndex:]



class StepResult(object):
  def __init__(self, startDate, years, months, days):
    self.balances = FastDateNumberList(days)
    self.addedInterests = FastDateNumberList(days)
    self.accumulatedIterests = FastDateNumberList(days+1)
    self.accumulatedIterests.append(startDate, 0.0)
    self.collectedInterests = FastDateNumberList(months)
    self.accumulatedCollectedInterests = FastDateNumberList(months+1)
    self.accumulatedCollectedInterests.append(startDate, 0.0)
    self.savings = FastDateNumberList(months)
    self.accumulatedSavings = FastDateNumberList(months+1)
    self.accumulatedSavings.append(startDate, 0.0)

  def addBalance(self, date, balance):
    self.balances.append(date, balance)

  def addInterest(self, date, interest):
    self.addedInterests.append(date, interest)
    self.accumulatedIterests.appendAccumulated(date, interest)

  def addCollectedInterest(self, date, collectedInterest):
    self.collectedInterests.append(date, collectedInterest)
    self.accumulatedCollectedInterests.appendAccumulated(date, collectedInterest)

  def addSaving(self, date, saving):
    self.savings.append(date, saving)
    self.accumulatedSavings.appendAccumulated(date, saving)

  def done(self):
    self.balances.done()
    self.addedInterests.done()
    self.accumulatedIterests.done()
    self.collectedInterests.done()
    self.accumulatedCollectedInterests.done()
    self.savings.done()
    self.accumulatedSavings.done()



class Stepper(object):
  def __init__(self):
    pass


  def stepAccounts(self, accounts, startDate, endDate, progressListener):
    # Worst case estimate of the number of years, months, and days that will be recorded.
    numYears = endDate.year - startDate.year + 1
    numMonths = numYears * 12
    numDays = numYears * 366

    # Create a result object for each account.
    results = []
    for account in accounts:
      results.append(StepResult(startDate, numYears, numMonths, numDays))

    # Setup a progress bar for long calculations.
    if progressListener != None:
      numYears = endDate.year - startDate.year
      if numYears > 10:
        progressListener.progressStarted(numYears)
      else:
        progressListener = None

    # Iterate through the dates.
    date = startDate
    aborted = False
    while date < endDate and not aborted:
      # Record current balance and interests for the current day.
      self.recordCurrentBalance(date, accounts, results)
      self.recordInterest(date, accounts, results)

      # Move to the next day.
      date += timedelta(days=1)

      # Specal handling for every new month.
      if date.day == 1:
        self.recordSavings(date, accounts, results)
        self.collectInterestsForLoans(date, accounts, results)

      # Special handling for every new year.
      if date.month == 1 and date.day == 1:
        self.collectInterestsForSavingAccounts(date, accounts, results)
        
        # Progress bar is updated on a per-year basis.
        if progressListener != None:
          currentYear = date.year - startDate.year
          aborted = progressListener.progressUpdate(currentYear)
    
    # Iteration is done, record final balance and truncate result lists.
    self.recordCurrentBalance(date, accounts, results)
    self.markAsDone(results)

    # Remove progress bar.
    if progressListener != None:
      progressListener.progressDone()

    return results




  def recordCurrentBalance(self, date, accounts, results):
    for index in range(0, len(accounts)):
      account = accounts[index]
      result = results[index]

      result.addBalance(date, account.getBalance())


  def recordInterest(self, date, accounts, results):
    if calendar.isleap(date.year):
      timeFraction = 1.0/366.0
    else:
      timeFraction = 1.0/365.0

    for index in range(0, len(accounts)):
      account = accounts[index]
      result = results[index]

      addedInterest = account.applyInterest(date, timeFraction)
      result.addInterest(date, addedInterest)


  def recordSavings(self, date, accounts, results):
    for index in range(0, len(accounts)):
      account = accounts[index]
      result = results[index]

      saving = account.addSaving(date)
      result.addSaving(date, saving)


  def collectInterestsForSavingAccounts(self, date, accounts, results):
    for index in range(0, len(accounts)):
      account = accounts[index]
      result = results[index]

      if not account.isLoan():
        collectedInterest = account.collectInterest()
        result.addCollectedInterest(date, collectedInterest)


  def collectInterestsForLoans(self, date, accounts, results):
    for index in range(0, len(accounts)):
      account = accounts[index]
      result = results[index]

      if account.isLoan():
        collectedInterest = account.collectInterest()
        result.addCollectedInterest(date, collectedInterest)




  def markAsDone(self, results):
    for result in results:
      result.done()

