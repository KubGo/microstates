from abc import ABC, abstractmethod
from .AbstractModel import AbstractModel
import numpy.typing as npt
from clustering.results import Results

class AbstractAnalysisStrategy(ABC):

    def __init__(self, model: AbstractModel, alpha: float, interpolMicrostates: bool):
        self.model = model
        self.alpha = alpha
        self.interpolMicrostates = interpolMicrostates

    @abstractmethod
    def perform_analysis(self) -> Results:
        pass

class WholeSignalAnalysisStrategy(AbstractAnalysisStrategy):

    def __init__(self, model, alpha, interpolMicrostates):
        super().__init__(model, alpha, interpolMicrostates)

    def perform_analysis(self, data: npt.ArrayLike):
        results = self.model.perform_analysis(
            data=data,
            clustering=True,
            alpha=self.alpha,
            interpolMicrostates=self.interpolMicrostates
        )
        return results
    
