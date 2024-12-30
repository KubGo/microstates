import os
import matplotlib.pyplot as plt

from pathlib import Path
from abc import ABC, abstractmethod
from clustering.models.abstractModel import AbstractModel
from test_data_readers.data_readers import AbstractDataReader
from test_data_readers.data_models import Data
from testing.utilities import split_data_at_time
from reporting import generate_comparison_report
from gui.results_observers import CurrentSessionResults
from clustering.models.abstractModel.analysis_strategies import AbstractAnalysisStrategy


class AbstractTest(ABC):

    def __init__(self, 
                analysis_strategy: AbstractAnalysisStrategy,
                data_reader: AbstractDataReader,
                current_session_results: CurrentSessionResults,
                ):
        self.data_reader = data_reader
        self.current_session_results = current_session_results
        self.analysis_strategy = analysis_strategy

    @abstractmethod
    def run(self, results_folder: str):
        pass

class GUITest(AbstractTest):
    def __init__(self, analysis_strategy, data_reader, current_session_results):
        super().__init__(analysis_strategy, data_reader, current_session_results)
    def run(self, results_folder):
        while self.data_reader.has_more():
            data = self.data_reader.next()
            
            results_path = Path().joinpath(results_folder,
                                        data.id,
                                        self.analysis_strategy.model.method,
                                        data.activity) 
            results_path.mkdir(parents=True, exist_ok=True)
            results_list = self.analysis_strategy.perform_analysis(
                data=data,
                path=results_path,
            )
            for res in results_list:
                self.current_session_results.add_new_current_session_result(res)
                self.current_session_results.update()
            

class Test:
    def __init__(self, model: AbstractModel, test_data: dict, break_time: float):
        self.model = model
        self.test_data = test_data
        self.break_time = break_time     

    def test_whole_data_separate_imagining(self, results_path, interpolateMicrostates=False, break_time_period = 2, fs = 250) -> None:
        
        if not os.path.exists(results_path):
            os.makedirs(results_path)
            
        testDescription = self.test_data['testDescription']
        data = self.test_data['data']
            
        # Get paths and model data
        method = self.model.method
        method_path = os.path.join(results_path, method)
        
        # Perform clustering and save general data
        results_whole_data = self.model.perform_analysis(data, 
                                    clustering=True, 
                                    interpolMicrostates=interpolateMicrostates)
        results_whole_data.generate_results_report(method_path,
                                                   method,
                                                   testDescription)
        
        
        listening_data, imagining_data = split_data_at_time(data, 
                                                            time=self.break_time, 
                                                            break_time_period=break_time_period, 
                                                            fs=fs)
        
        # Perform analysis for imagining with listening to the transcript
        results_listening = self.model.perform_analysis(listening_data,
                                    clustering=False,
                                    interpolMicrostates=interpolateMicrostates)
        
        # Save results
        results_listening.generate_results_report(method_path,
                                                method,
                                                testDescription,
                                                subfolder="listening")
        
        results_imagining = self.model.perform_analysis(imagining_data, 
                                    clustering=False,
                                    interpolMicrostates=interpolateMicrostates)
        
        results_imagining.generate_results_report(method_path, 
                                                  method,
                                                  testDescription,
                                                  subfolder="imagining")
        
        # Generate comparison report
        generate_comparison_report(method_path)
        plt.close()

    def test_data_separatly(self, results_path, interpolateMicrostates=False, break_time_period = 2, fs = 250) -> None:
        if not os.path.exists(results_path):
            os.makedirs(results_path)
            
        testDescription = self.test_data['testDescription']
        data = self.test_data['data']
            
        # Get paths and model data
        method = self.model.method
        method_path = os.path.join(results_path, method)
        
        listening_data, imagining_data = split_data_at_time(data, 
                                                            time=self.break_time, 
                                                            break_time_period=break_time_period, 
                                                            fs=fs)
        
        results_listening = self.model.perform_analysis(listening_data,
                                    clustering=True,
                                    interpolMicrostates=interpolateMicrostates)
        
        results_listening.generate_results_report(method_path,
                                                method,
                                                testDescription,
                                                subfolder="listening")
        
        results_imagining = self.model.perform_analysis(imagining_data, 
                                    clustering=True,
                                    interpolMicrostates=interpolateMicrostates)
        
        results_imagining.generate_results_report(method_path, 
                                                  method,
                                                  testDescription,
                                                  subfolder="imagining")
        
        # Generate comparison report
        generate_comparison_report(method_path, separate_states=True)
        plt.close()
    