from abc import ABC, abstractmethod
from clustering.models.abstractModel import AbstractModel
from clustering.results import Results
import numpy.typing as npt

class AbstractTestingSrategy(ABC):

    def __init__(self, model: AbstractModel,
                data: npt.ArrayLike,
                interpol:bool=True,
                alpha:float=0.01):
        super().__init__()
        self.model = model
        self.data = data
        self.interpol = interpol
        self.alpha = alpha
        self.folder = ""

    @abstractmethod
    def test(self) -> Results:
        pass

class WholeDataTest(AbstractTestingSrategy):
    def __init__(self, model, data, interpol, alpha):
        super().__init__(model, data, interpol, alpha)
        self.folder = "wholeDataTest"

    def test(self):
        results = self.model.perform_analysis(
            data=self.data,
            clustering=True,
            alpha=self.alpha,
            interpolMicrostates=self.interpol
        )
