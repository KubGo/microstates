import os
from . ParticipantTests import Participant

class GroupTests:
    
    def __init__(self, path_to_folder,
                 methods=('kmeans', 'pca', 'ica', 'kmedoids', 'aahc'),
                 break_times_dict = None):
        self.methods = methods
        self.break_times_dict = break_times_dict
        self.participants = [
            self.get_participant(os.path.join(path_to_folder, folder))
            for folder in os.listdir(path_to_folder) if os.path.isdir(os.path.join(path_to_folder, folder))
        ]
    
    def get_participant(self,path_to_participant):
        return Participant(path_to_participant,
                           methods=self.methods,
                           break_times_dict=self.break_times_dict)
    
    def run_group_tests(self, results_path,
                        tests_to_perform = ('wholeDataSeparateImagining','separateData'),
                        interpolate_microstates=False,
                        break_time_period = 2, 
                        fs = 250):
        if not os.path.exists(results_path):
            os.makedirs(results_path)
        for participant in self.participants:
            participant.runTests(
                results_path,
                tests_to_perform=tests_to_perform,
                interpolate_microstates=interpolate_microstates,break_time_period=break_time_period,
                fs=fs)