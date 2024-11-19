import numpy as np
from dataPreparing import prepare_file


class SignalCleaner:
    """Signal cleaner that deletes time in seconds from start and end of the signal
    """
    
    def __init__(self, time_start: float, time_end: float, frequency: int):
        self.frequency = frequency
        self.time_start = time_start
        self.time_end = time_end
    
    def clean_file(self, path_to_file: str) -> np.array:
        """Clean file

        Args:
            path_to_file (str): Path to a file

        Returns:
            np.array: Data for clustering
        """
        clean_data = prepare_file(
            path_to_file=path_to_file,
            time_start=self.time_start,
            time_end=self.time_end,
            fs=self.frequency) 
        return clean_data