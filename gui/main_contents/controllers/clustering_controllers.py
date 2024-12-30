from abc import ABC, abstractmethod
from gui.controllers.interfaces import AbstractController
from clustering.models import model_factory
from clustering.models.abstractModel import AbstractModel
from clustering.models.abstractModel.analysis_strategies import AbstractAnalysisStrategy, WholeSignalAnalysisStrategy, TwoGroupsSeparateMicrostates
from test_data_readers.data_readers import AbstractDataReader, FileDataReader
from test_data_readers.data_identifiers import AbstractDataIdentifier, DelimiteredDataIdentifier, FilePathDataIdentifier
from test_data_readers.data_read_strategies import AbstractDataReadStrategy, CleanDataReadStrategy, DeleteStartEndDataStrategy
from testing import GUITest
from gui.main_contents.clustering_page import ClusteringPageContent
from gui.results_observers import  AbstractResultsObserver
from test_data_readers.data_splitters import TwoGroupsSplitter


class AbstractClusteringControler(AbstractController, AbstractResultsObserver):

    def __init__(self, view: ClusteringPageContent):
        super().__init__(view)
        self.view = view
        self.view.update_controller(self)

    @abstractmethod
    def cluster(self):
        pass

    @abstractmethod
    def update_view(self):
        pass

class ClusteringController(AbstractClusteringControler):
    def __init__(self, view: ClusteringPageContent):
        super().__init__(view)

    def cluster(self):
        self.view.clustering_done_text.visible = False
        self.view.clustering_done_text.update()
        model = self.get_clustering_model()
        data_reader = self.get_data_reader(model)

        analysis_strategy = self.get_analysis_strategy(
            model=model,
            alpha=0.01,
            interpolMicrostates=self.view.clustering_settings_section.use_interpolation.value,
        )
        test = GUITest(
            analysis_strategy=analysis_strategy,
            data_reader=data_reader,
            current_session_results = self.current_session_results,
        )

        test.run("./prototyping/guitest")
        self.update_view()

    def get_analysis_strategy(self, model, alpha, interpolMicrostates) -> AbstractAnalysisStrategy:
        value = self.view.clustering_settings_section.analysis_strategy.value
        if value == 'two_groups_common_microstates':
            print("dupa")
            return WholeSignalAnalysisStrategy(
                model=model,
                alpha=alpha,
                interpolMicrostates=interpolMicrostates,
            )
        elif value == 'two_groups_separate_microstates':
            return TwoGroupsSeparateMicrostates(
                model=model,
                alpha=alpha,
                interpolMicrostates=interpolMicrostates,
                splitter=TwoGroupsSplitter(
                    frequency=int(self.view.select_files_section.frequency_entry.value),
                    break_time_period=2,
                    break_times_dict= {
                        'Successful_Competition': 38,
                        'Fitness_Activity': 37,
                        'Slow_Start': 47,
                        'Start_high_level_championship': 33,
                        'Training_Session': 37,
                        'Your_Home_Venue': 40
                    },
                )
            )
        else:
            return WholeSignalAnalysisStrategy(
                model=model,
                alpha=alpha,
                interpolMicrostates=interpolMicrostates,
            )

    def update_view(self):
        self.view.clustering_done_text.value = "Clustering done!"
        self.view.clustering_done_text.visible = True

    def results_update(self):
        print("Results update from clustering controller :)")

        
    def get_clustering_model(self) -> AbstractModel:
        model = model_factory(
            method= self.view.clustering_settings_section.clustering_alogorithm_selector.value,
            f_sampling=self.view.select_files_section.frequency_entry.value,
            n_maps=4,
        )
        return model
    
    def get_data_identifier(self) -> AbstractDataIdentifier:
        if self.view.use_delimiters_checkbox.value:
            delimiters_settings = self.view.delimiters_section
            delimiter = delimiters_settings.delimiter_selector.value
            id_index = int(delimiters_settings.id_index_entry.value) - 1
            activity_index = int(delimiters_settings.activity_index_entry.value) - 1
            return DelimiteredDataIdentifier(
                delimiter=delimiter,
                id_position=id_index,
                activity_position=activity_index
            )
        return FilePathDataIdentifier()
    
    def get_data_read_strategy(self) -> AbstractDataReadStrategy:
        frequency = self.view.select_files_section.frequency_entry.value
        if self.view.use_signals_cutting_checkbox.value:
            cutting_settings = self.view.signal_cutting_section
            start_time = 0
            end_time = 0
            if cutting_settings.checkbox_start_signal.value:
                start_time = int(cutting_settings.signal_start_entry.value)
            if cutting_settings.checkbox_end_signal.value:
                end_time = int(cutting_settings.signal_end_entry.value)

            return DeleteStartEndDataStrategy(
                frequency=frequency,
                start_time=start_time,
                end_time=end_time
            )
        return CleanDataReadStrategy(frequency=frequency)
    

    def get_data_reader(self, model: AbstractModel) -> AbstractDataReader:    
        clustering_model = model
        data_identifier = self.get_data_identifier()
        data_read_strategy = self.get_data_read_strategy()
        data_reader = FileDataReader(
            data_read_strategy=data_read_strategy,
            data_identifier=data_identifier
        )

        data: list[str] = self.view.select_files_section.selected_files.get_file_paths()
        for file in data:
            data_reader.add_data(file)

        return data_reader
    

