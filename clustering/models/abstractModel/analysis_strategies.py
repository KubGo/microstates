from abc import ABC, abstractmethod
from .AbstractModel import AbstractModel
import numpy.typing as npt
from clustering.results import Results
from test_data_readers.interfaces import AbstractDataSplitter
from test_data_readers.data_models import Data
from reporting import generate_comparison_report

class AbstractAnalysisStrategy(ABC):

    def __init__(self, model: AbstractModel, alpha: float, interpolMicrostates: bool):
        self.model = model
        self.alpha = alpha
        self.interpolMicrostates = interpolMicrostates

    @abstractmethod
    def perform_analysis(self, data: Data, path: str) -> list[Results]:
        pass

class WholeSignalAnalysisStrategy(AbstractAnalysisStrategy):

    def __init__(self, model, alpha, interpolMicrostates):
        super().__init__(model, alpha, interpolMicrostates)

    def perform_analysis(self, data: Data, path: str):
        results = self.model.perform_analysis(
            data=data.data,
            clustering=True,
            alpha=self.alpha,
            interpolMicrostates=self.interpolMicrostates
        )
        results.set_id_and_activity(data.id, data.activity)

        results.generate_results_report(
            destination_path=path,
            method=results.method,
            activity=data.activity
        )
        return [results]
    
class TwoGroupsSeparateMicrostates(AbstractAnalysisStrategy):

    def __init__(self, model, alpha, interpolMicrostates, splitter):
        super().__init__(model, alpha, interpolMicrostates)
        self.splitter = splitter

    def perform_analysis(self, data: Data, path: str, folder_names: list[str]=['before', 'after']):
        split_data_list = self.splitter.split_data(data)
        before_split_data = split_data_list[0]
        after_split_data = split_data_list[1]

        results_before_split = self.model.perform_analysis(
            data=before_split_data,
            clustering=True,
            interpolMicrostates=self.interpolMicrostates,
            alpha=self.alpha,
        )
        results_before_split.generate_results_report(
            destination_path=path,
            subfolder=folder_names[0],
            method=self.model.method,
            activity=data.activity,
        )
        results_before_split.set_id_and_activity(f"{data.id}-before", data.activity)

        results_after_split = self.model.perform_analysis(
            data=after_split_data,
            clustering=True,
            interpolMicrostates=self.interpolMicrostates,
            alpha=self.alpha
        )
        results_after_split.generate_results_report(
            destination_path=path,
            method=self.model.method,
            activity=data.activity,
            subfolder=folder_names[1]
        )
        results_after_split.set_id_and_activity(f"{data.id}-after", data.activity)

        generate_comparison_report(
            path_to_folder=path,
            separate_states=True,
            folder_names=folder_names,
        )
        return [results_before_split, results_after_split]
