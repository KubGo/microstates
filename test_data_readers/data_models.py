import numpy.typing as npt

class Data:
    """Data class that holds id, activity and numpy data of the signal
    """
    def __init__(self, id: str, activity: str, data: npt.ArrayLike):
        self.id = id
        self.activity = activity
        self.data = data

    __dict__ = ['id', 'activity', 'data']
    