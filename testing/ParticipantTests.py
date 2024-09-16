import os
from dataPreparing import readTestFiles
from clustering.models import model_factory
from testing import Test

BREAKS_TIMES_DICT = {

    'Successful_Competition': 38,

    'Fitness_Activity': 37,

    'Slow_Start': 47,

    'Start_high_level_championship': 33,

    'Training_Session': 37,

    'Your_Home_Venue': 40

}
class Participant:
    
    def __init__(self, path_to_participant_data,
                 methods = ('kmeans', 'pca', 'ica', 'kmedoids', 'aahc'),
                 break_times_dict = None):
        self.tests_data = self.get_tests_data(path_to_participant_data)
        self.name = os.path.split(path_to_participant_data)[-1]
        if break_times_dict is None:
            self.break_times_dict = BREAKS_TIMES_DICT
        self.methods = methods
        
    def runTests(self, results_path, 
                 tests_to_perform = ('wholeDataSeparateImagining','separateData'),
                 interpolate_microstates=False,
                 break_time_period = 2, 
                 fs = 250) -> None:
        if not os.path.exists(results_path):
            os.makedirs(results_path)
        # Test for each method
        for method in self.methods:
            model = model_factory(self.name, method)
            
            # Test for each test activity
            for test_data in self.tests_data:
                test_description = test_data['testDescription']
                break_time = self.get_break_time(test_description)
                test = Test(model,
                            test_data=test_data,
                            break_time=break_time)
                # Run tests
                
                if 'wholeDataSeparateImagining' in tests_to_perform:
                    path_to_save = os.path.join(
                        results_path, 
                        self.name,
                        test_description,
                        'wholeDataSeparateImagining')
                    test.test_whole_data_separate_imagining(
                        path_to_save,
                        interpolateMicrostates=interpolate_microstates,
                        break_time_period=break_time_period,
                        fs=fs)
                if 'separateData' in tests_to_perform:
                    path_to_save = os.path.join(
                        results_path,
                        self.name,
                        test_description,
                        'separateData')
                    test.test_data_separatly(
                        path_to_save,
                        interpolateMicrostates=interpolate_microstates,
                        break_time_period=break_time_period,
                        fs=fs)

    def get_tests_data(self, path_to_participant_data):
        if not os.path.exists(path_to_participant_data):
            raise FileNotFoundError(f"There is no such a directory: {path_to_participant_data}.")
        return readTestFiles(path_to_participant_data)
    
    def get_break_time(self, testDescription: str):
        for test_name, break_time in self.break_times_dict.items():
            if (str(test_name).lower().find(testDescription.lower())) >= 0:
                return break_time
        raise ReferenceError(f"Did not find the break time for {testDescription}.")