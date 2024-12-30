from .interfaces import AbstractDataSplitter
import numpy.typing as npt
from test_data_readers.data_models import Data
from testing.utilities import split_data_at_time

class TwoGroupsSplitter(AbstractDataSplitter):
    
    def __init__(self, frequency, break_times_dict, break_time_period):
        super().__init__(frequency, break_times_dict, break_time_period)

    def split_data(self, data: Data):
        activity = data.activity
        time = self.get_break_time(activity)
        before, after = split_data_at_time(
            data=data.data,
            time=time,
            break_time_period=self.break_time_period,
            fs=self.frequency
        )
        return [before, after]
    
    def get_break_time(self, activity: str):
        for test_name, break_time in self.break_times_dict.items():
            if (str(test_name).lower().find(activity.lower())) >= 0:
                return break_time
