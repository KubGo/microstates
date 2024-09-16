import numpy as np

def split_data_at_time(data: np.array, time: float, break_time_period = 2, fs=250):
    """Splits data at given time

    Args:
        data (np.array): Data to split
        time (float): Time to split data
        break_time (float): Time of break. Defaults to 2.
        fs (int, optional): Sampling frequency of the data. Number of data points captured per second. Defaults to 250.

    Returns:
        np.array: returns two np.arrays with data before and after the break
    """
    break_sample = int(time * fs)
    resume_sample = break_sample + int(break_time_period * fs)
    data_before_break = data[:break_sample, :]
    data_after_break = data[resume_sample:, :]
    return data_before_break, data_after_break