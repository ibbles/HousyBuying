#!/usr/bin/python

from Accounts import Account
from Interest import Interest
from Interest import InterestRate
from NumberSequences import StepNumber

import datetime

interestAtDate_data = [
  (datetime.date(2014, 1, 1), 1.0),
  (datetime.date(2014, 2, 1), 1.0),
  (datetime.date(2014, 3, 1), 1.0),
  (datetime.date(2014, 4, 1), 1.0),
  (datetime.date(2014, 5, 1), 1.0),
  (datetime.date(2015, 3, 1), 1.0),
  (datetime.date(2015, 8, 1), 1.0),
  (datetime.date(2016, 2, 1), 1.0),
  (datetime.date(2016, 5, 1), 1.0)
]
interestAtDate = StepNumber(interestAtDate_data)
interestRate = InterestRate(interestAtDate)
interest = Interest(interestRate);

payingAccount = Account()
payingAccount = payingAccount.deposit(20)
print("At start of time: Balance = {0:.2f}, interest={1:.2f}.".format(payingAccount.getBalance(), payingAccount.getStoredInterest()))
for year in range(2014, 2019):
  for month in range(1,13):
    date = datetime.date(year, month, 1)
    payingAccount = payingAccount.applyInterest(interest, date, 1.0/12.0)
    print("At end of month {0}-{1:02d}: Balance = {2:.2f}, interest={3:.2f}.".format(year, month, payingAccount.getBalance(), payingAccount.getStoredInterest()))
  payingAccount = payingAccount.collectInterest()
  print("At end of year {0}: Balance = {1:.2f}, interest={2:.2f}.".format(year, payingAccount.getBalance(), payingAccount.getStoredInterest()))
print("At end of time: Balance = {0:.2f}, interest={1:.2f}.".format(payingAccount.getBalance(), payingAccount.getStoredInterest()))