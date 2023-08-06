from os import listdir
from os.path import isfile, join

import pandas as pd


class FileReader:
    @classmethod
    def readFolder(cls, path):
        dfs = []
        for filename in listdir(path):
            if isfile(join(path, filename)) and filename.endswith(cls.fileExt):
                df = cls.readFile(join(path, filename))
                dfs.append(df)

        return pd.concat(dfs, ignore_index=True)

    @classmethod
    def readFile(cls, filename):
        """Implement in subclass."""
        raise NotImplementedError

    @classmethod
    def isIncome(cls, row):
        if row[cls.amountColIndex] >= 0:
            return row[cls.amountColIndex]
        return 0

    @classmethod
    def isOutcome(cls, row):
        if row[cls.amountColIndex] < 0:
            return -row[cls.amountColIndex]
        return 0


class DefaultFileReader(FileReader):
    fileExt = ".csv"
    amountColIndex = 2

    @classmethod
    def readFile(cls, filename):
        df = pd.read_csv(filename)
        df["Income"] = df.apply(cls.isIncome, axis=1)
        df["Outcome"] = df.apply(cls.isOutcome, axis=1)
        df = df.drop(df.columns[[2]], axis=1)
        df.columns = ["Date", "Concept", "Income", "Outcome"]
        df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y")  # noqa: WPS323
        return df.sort_values(by="Date")
