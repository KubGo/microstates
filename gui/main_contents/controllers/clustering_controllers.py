from abc import ABC, abstractmethod
from gui.controllers.interfaces import AbstractController
from clustering.models import model_factory
from clustering.models.abstractModel import AbstractModel
from test_data_readers.data_readers import AbstractDataReader, FileDataReader
from test_data_readers.data_identifiers import AbstractDataIdentifier, DelimiteredDataIdentifier, FilePathDataIdentifier
from test_data_readers.data_read_strategies import AbstractDataReadStrategy, CleanDataReadStrategy, DeleteStartEndDataStrategy
from testing import WholeDataTest
from gui.main_contents.clustering_page import ClusteringPageContent

class AbstractClusteringControler(AbstractController):

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
    
class WholeSignalClusteringControler(AbstractClusteringControler):
    def __init__(self, view: ClusteringPageContent):
        super().__init__(view)

    def cluster(self):
        self.view.clustering_done_text.visible = False
        self.view.clustering_done_text.update()
        model = self.get_clustering_model()
        data_reader = self.get_data_reader(model)

        test = WholeDataTest(
            model=model,
            data_reader=data_reader,
            interpol_microstates=self.view.clustering_settings_section.use_interpolation.value
        )

        test.run("./prototyping/guitest")
        self.update_view()

    def update_view(self):
        self.view.clustering_done_text.value = "Clustering done!"
        self.view.clustering_done_text.visible = True
        self.view.clustering_done_text.update()

        
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
    

