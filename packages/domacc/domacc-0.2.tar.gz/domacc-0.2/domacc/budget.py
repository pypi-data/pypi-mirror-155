import datetime

import pandas as pd


class Budget:
    """Frequencies: daily (D) weekly (W) monthly (M) year (Y)."""

    def __init__(self, accounting, categories, frequency, limit):
        accounting = self.filterAccountingByCategories(accounting, categories)
        self.limit = limit
        self.periodicOutcome = self.getPeriodicOutcome(accounting, frequency)

    @classmethod
    def filterAccountingByCategories(cls, accounting, categories):
        for category in categories:
            mask = accounting["Tags"].str.contains(category)
            accounting = accounting.loc[mask]
        return accounting

    @classmethod
    def getMeanBasedBudget(cls, accounting, categories, frequency):
        accounting = cls.filterAccountingByCategories(accounting, categories)
        periodicOutcome = cls.getPeriodicOutcome(accounting, frequency)
        return cls(accounting, categories, frequency, periodicOutcome.mean())

    @classmethod
    def getPeriodicOutcome(cls, accounting, frequency):
        periodicOutcome = []
        periodRange = pd.period_range(
            start=accounting.iloc[0]["Date"], end=accounting.iloc[-1]["Date"], freq=frequency
        )
        for period in periodRange:
            mask1 = accounting["Date"] >= period.start_time
            mask2 = accounting["Date"] <= period.end_time
            df = accounting.loc[mask1 & mask2]
            periodicOutcome.append(sum(df["Outcome"]))
        return pd.DataFrame(periodicOutcome, index=periodRange)

    def getPeriodicRemaining(self):
        return self.limit - self.periodicOutcome

    def getCurrentRemaining(self):
        remaining = self.getPeriodicRemaining()
        now = datetime.datetime.now()
        for date, row in remaining.iterrows():
            if date.start_time <= now <= date.end_time:
                return row[0]

        return self.limit
