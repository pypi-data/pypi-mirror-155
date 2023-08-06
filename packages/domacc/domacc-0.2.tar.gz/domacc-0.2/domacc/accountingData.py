import importlib
import sys
from pathlib import Path

import pandas as pd

from domacc.fileReader import DefaultFileReader


class AccountingData:
    def __init__(self, name, path, readerType, initialCash=0, customReaders=None):
        self.name = name
        self.path = path
        self.reader = self._getFileReader(readerType, customReaders)
        self.initialCash = initialCash

    @classmethod
    def LoadFromJsonObject(cls, accDataDict, customReaders, configFile):
        name = accDataDict.get("id")
        path = cls._getFullPath(accDataDict.get("bankMovesPath"), configFile)
        readerType = accDataDict.get("readerType")
        initialCash = accDataDict.get("initialCash")
        customReaders = cls._getFullPath(customReaders, configFile)
        return cls(name, path, readerType, initialCash, customReaders)

    @classmethod
    def _getFullPath(cls, path, configFile):
        path = Path(path)
        if not path.is_absolute():
            parent = Path(configFile).parent
            path = parent / path
        return path

    def _getFileReader(self, readerType, customReaders):
        if readerType == "DefaultFileReader":
            return DefaultFileReader
        if customReaders:
            customReaders = Path(customReaders).absolute()
            sys.path.append(str(customReaders.parent))
            try:
                readers = importlib.import_module(customReaders.stem)
            except ImportError:
                raise ValueError(f"Error importing custom reader {readerType}")

            try:
                reader = getattr(readers, readerType)
            except AttributeError:
                raise ValueError(f"Error importing custom reader {readerType}")
        return reader

    def getMovements(self):
        movements = self.reader.readFolder(self.path)
        if self.initialCash:
            initialCashDF = pd.DataFrame(
                {
                    "Date": [movements.iloc[0]["Date"]],
                    "Concept": ["Initial cash"],
                    "Income": [max(0, self.initialCash)],
                    "Outcome": [max(0, -self.initialCash)],
                }
            )
            movements = pd.concat([initialCashDF, movements], ignore_index=True)

        movements["AccountId"] = self.name
        return movements
