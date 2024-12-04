import numpy.typing as npt

class Data:
    def __init__(self, id: str, activity: str, data: npt.ArrayLike):
        self.id = id
        self.activity = activity
        self.data = data

    __dict__ = ['id', 'activity', 'data']
    