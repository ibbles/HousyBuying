
from datetime import timedelta
import calendar

import sys

def log(message):
  sys.stdout.write(message)

class Stepper(object):
  def __init__(self):
    pass


  def stepAccount(self, account, startDate, endDate):
    dates = []
    balances = []
    addedInterests = []
    collectedInterests = []

    date = startDate
    while date < endDate:
      log("Start of date {}, balance is {}.".format(date, account.getBalance()),)
      dates.append(date)
      balances.append(account.getBalance())
      if calendar.isleap(date.year):
        timeFraction = 1.0/366.0
      else:
        timeFraction = 1.0/365.0
      addedInterest = account.applyInterest(date, timeFraction)
      addedInterests.append(addedInterest)
      log(" Got {} interest. Have stored {}.".format(addedInterest, account.getStoredInterest()))
      date += timedelta(days=1)
      if (date.month == 1 and date.day == 1):
        collectedInterest = account.collectInterest()
        collectedInterests.append(collectedInterest)
        log(" It is a new year. Collected {} in interest. New balance is {}.".format(collectedInterest, account.getBalance()))
      log("\n")
    
    dates.append(date)
    balances.append(account.getBalance())
    return dates, balances, addedInterests, collectedInterests


    # <NumberSequences.DateNumberList object at 0x8444a50>
