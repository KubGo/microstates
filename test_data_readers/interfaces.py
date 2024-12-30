from abc import ABC, abstractmethod
from test_data_readers.data_models import Data
import numpy.typing as npt

class AbstractDataSplitter(ABC):
    def __init__(self, frequency: int, break_times_dict: dict, break_time_period: float):
        self.frequency = frequency
        self.break_times_dict = break_times_dict
        self.break_time_period = break_time_period

    @abstractmethod
    def split_data(self, data: Data) -> list[npt.ArrayLike]:
        pass