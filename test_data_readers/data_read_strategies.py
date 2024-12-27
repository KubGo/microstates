from abc import ABC, abstractmethod
from . data_identifiers import AbstractDataIdentifier
import pandas as pd
import numpy.typing as npt

class AbstractDataReadStrategy(ABC):
    """Interface for reading data strategies
    """

    def __init__(self, frequency: int):
        self.frequency = frequency

    @abstractmethod
    def get_data(self, file_path: str) -> npt.ArrayLike:
        """Gets EEG signal from file

        Args:
            file_path (str): Path to a file

        Returns:
            npt.ArrayLike: Signal in numpy array format
        """
        pass


class CleanDataReadStrategy(AbstractDataReadStrategy):
    """Reads clean data, that doesn't need any operations on it
    """
    
    def __init__(self, frequency):
        super().__init__(frequency)

    def get_data(self, file_path):
        return pd.read_csv(file_path, index_col=0).to_numpy()
    
class DeleteStartEndDataStrategy(AbstractDataReadStrategy):
    """Delets given time from start and end of the signal
    """

    def __init__(self, frequency, start_time: float, end_time: float):
        self.start_time = start_time
        self.end_time = end_time
        super().__init__(frequency)

    def get_data(self, file_path):
        data = pd.read_csv(file_path, index_col=0)
        start_sample = round(self.start_time * self.frequency)
        end_sample = round(self.end_time * self.frequency)
        clean_data = data.iloc[start_sample: -end_sample, :]
        return clean_data.to_numpy()

