
from datetime import timedelta
import calendar

import sys

def log(message):
  pass
  #sys.stdout.write(message)


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


  def stepAccounts(self, accounts, startDate, endDate):
    results = []
    for account in accounts:
      results.append(StepResult())

    date = startDate
    while date < endDate:
      for index in range(0, len(accounts)):
        account = accounts[index]
        result = results[index]

        log("Start of date {}, balance is {}.".format(date, account.getBalance()),)
        
        # Store the current date and balance.
        result.dates.append(date)
        result.balances.append(account.getBalance())
        if calendar.isleap(date.year):
          timeFraction = 1.0/366.0
        else:
          timeFraction = 1.0/365.0
        
        # Add interest for the current day.
        addedInterest = account.applyInterest(date, timeFraction)
        result.addedInterests.append(addedInterest)
        log(" Got {} interest. Have stored {}.".format(addedInterest, account.getStoredInterest()))
        
        # Move to next day.
        date += timedelta(days=1)
        
        if date.day == 1:
          # New month, add saving.
          saving = account.addSaving(date)
          result.savings.append(saving)


        if date.month == 1 and date.day == 1:
          # New year, collect interest.
          collectedInterest = account.collectInterest()
          result.collectedInterests.append(collectedInterest)
          log(" It is a new year. Collected {} in interest. New balance is {}.".format(collectedInterest, account.getBalance()))

        log("\n")
    
    for index in range(0, len(accounts)):
      account = accounts[index]
      result = results[index]
      result.dates.append(date)
      result.balances.append(account.getBalance())

    return results


    # <NumberSequences.DateNumberList object at 0x8444a50>
