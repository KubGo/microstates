import os
import matplotlib.pyplot as plt


from clustering.models.abstractModel import AbstractModel
from testing.utilities import split_data_at_time
from reporting import generate_comparison_report



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
    