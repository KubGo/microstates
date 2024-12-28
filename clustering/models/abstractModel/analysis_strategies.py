from abc import ABC, abstractmethod
from .AbstractModel import AbstractModel
import numpy.typing as npt
from clustering.results import Results
from test_data_readers.data_splitters import AbstractDataSplitter, TwoGroupsSplitter
from test_data_readers.data_models import Data

class AbstractAnalysisStrategy(ABC):

    def __init__(self, model: AbstractModel, alpha: float, interpolMicrostates: bool):
        self.model = model
        self.alpha = alpha
        self.interpolMicrostates = interpolMicrostates

    @abstractmethod
    def perform_analysis(self, data: Data) -> Results:
        pass

class WholeSignalAnalysisStrategy(AbstractAnalysisStrategy):

    def __init__(self, model, alpha, interpolMicrostates):
        super().__init__(model, alpha, interpolMicrostates)

    def perform_analysis(self, data: Data):
        results = self.model.perform_analysis(
            data=data.data,
            clustering=True,
            alpha=self.alpha,
            interpolMicrostates=self.interpolMicrostates
        )
        return results
    
class TwoGroupsSeparateMicrostates(AbstractAnalysisStrategy):

    def __init__(self, model, alpha, interpolMicrostates, splitter: AbstractDataSplitter):
        super().__init__(model, alpha, interpolMicrostates)
        self.splitter = splitter

    def perform_analysis(self, data):
        split_data_list = self.splitter.split_data(data.data)
        before_split_data = split_data_list[0]
        after_split_data = split_data_list[1]

        results_before_split = self.model.perform_analysis(
            data=before_split_data,
            clustering=True,
            interpolMicrostates=self.interpolMicrostates,
            alpha=self.alpha,
        )
        results_before_split.generate_results_report(
            subfolder="before",
            method=self.model.method,
            activity=data.activity,
        )

        results_after_split = self.model.perform_analysis(
            data=after_split_data,
            clustering=True,
            interpolMicrostates=self.interpolMicrostates,
            alpha=self.alpha
        )
