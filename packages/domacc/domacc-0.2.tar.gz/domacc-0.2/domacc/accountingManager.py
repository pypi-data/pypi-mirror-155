import json
import logging
import re

import pandas as pd

from domacc.accountingData import AccountingData


class AccountingManager:
    def __init__(self, accountingData, categories):
        self.accounting = self._populateAccounting(accountingData, categories)

    @classmethod
    def LoadFromJsonFile(cls, configFile):
        with open(configFile) as jsonFile:
            jsonData = json.load(jsonFile)
            accountingData = cls._getAccountingData(jsonData, configFile)
            categories = jsonData.get("categories", {})
        return cls(accountingData, categories)

    @classmethod
    def _getAccountingData(cls, jsonData, configFile):
        accountingDatas = []
        customReaders = jsonData.get("customReaders")
        for accDataDict in jsonData["data"]:
            try:
                accountingData = AccountingData.LoadFromJsonObject(
                    accDataDict, customReaders, configFile
                )
            except Exception as error:
                logging.error(str(error))
            else:
                accountingDatas.append(accountingData)
        return accountingDatas

    def _populateAccounting(self, accountingData, categories):
        accounting = self._getMovements(accountingData)
        accounting = self.addBalance(accounting)
        return self.addCategories(accounting, categories)

    def _getMovements(self, accountingData):
        dfs = []
        for accData in accountingData:
            dfs.append(accData.getMovements())

        df = pd.concat(dfs, ignore_index=True)
        df = df.sort_values(by="Date")
        df.index = range(len(df))
        return df

    def addBalance(self, accounting):
        accounting["Balance"] = 0
        for index, _ in accounting.iterrows():
            previousBalance = accounting.loc[index - 1, "Balance"] if index else 0
            income = accounting.loc[index, "Income"]
            outcome = accounting.loc[index, "Outcome"]
            accounting.loc[index, "Balance"] = previousBalance + income - outcome
        return accounting

    def addCategories(self, accounting, categories):
        accounting["Tags"] = ""
        for index, row in accounting.iterrows():
            newTags = []
            for category in categories:
                if re.search(category["regex"], row["Concept"]):
                    newTags.extend(category["tags"])
            accounting.at[index, "Tags"] = ",".join(set(newTags))
        return accounting

    def getAccounting(self, initialDate=None, finalDate=None):
        accounting = self.accounting.copy(deep=True)
        if initialDate:
            mask = accounting["Date"] >= initialDate
            accounting = accounting.loc[mask]
        if finalDate:
            mask = accounting["Date"] <= finalDate
            accounting = accounting.loc[mask]
        accounting.index = range(len(accounting))
        return self.addBalance(accounting)
