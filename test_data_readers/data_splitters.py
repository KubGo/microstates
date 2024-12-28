from abc import ABC, abstractmethod
import numpy.typing as npt
from test_data_readers.data_models import Data
from testing.utilities import split_data_at_time

class AbstractDataSplitter(ABC):
    def __init__(self, frequency: int, break_times_dict: dict, break_time_period: float):
        self.frequency = frequency
        self.break_times_dict = break_times_dict
        self.break_time_period = break_time_period

    @abstractmethod
    def split_data(self, data: Data) -> list[npt.ArrayLike]:
        pass

    
class TwoGroupsSplitter(AbstractDataSplitter):
    
    def __init__(self, frequency, break_times_dict, break_time_period):
        super().__init__(frequency, break_times_dict, break_time_period)

    def split_data(self, data: Data):
        activity = data.activity
        time = self.break_times_dict[activity]
        before, after = split_data_at_time(
            data=data.data,
            time=time,
            break_time_period=self.break_time_period,
            fs=self.frequency
        )
        return [before, after]
