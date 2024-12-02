from abc import ABC, abstractmethod
from data_identifiers import AbstractDataIdentifier
import pandas as pd
import numpy.typing as npt

class AbstractData(ABC):

    def __init__(self, file_path: str, frequency: int, data_identifier: AbstractDataIdentifier):
        self.file_path = file_path
        self.id = data_identifier.get_id()
        self.activity = data_identifier.get_activity()
        self.frequency = frequency
        self.data = self.get_data()

    @abstractmethod
    def get_data(self, file_path) -> npt.ArrayLike:
        pass


class CleanData(AbstractData):
    
    def __init__(self, file_path, frequency, data_identifier):
        super().__init__(file_path, frequency, data_identifier)

    def get_data(self, file_path):
        return pd.read_csv(file_path, index_col=0).to_numpy()
    
class DirtyData(AbstractData):
    def __init__(self, file_path, frequency, data_identifier, start_time: float, end_time: float):
        self.start_time = start_time
        self.end_time = end_time
        super().__init__(file_path, frequency, data_identifier)

    def get_data(self, file_path):
        data = pd.read_csv(file_path, index_col=0)
        start_sample = round(self.start_time * self.frequency)
        end_sample = round(self.end_time * self.frequency)
        clean_data = data.iloc[start_sample: -end_sample, :]
        return clean_data.to_numpy()

