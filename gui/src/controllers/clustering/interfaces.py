from abc import ABC, abstractmethod
from controllers.interfaces import AbstractController
from ...main_contents.clustering_page import ClusteringPageContent
from clustering.models import model_factory
from clustering.models.abstractModel import AbstractModel

class AbstractClusteringControler(AbstractController):

    def __init__(self, content: ClusteringPageContent):
        super().__init__(self, content)
        self.content = content

    @abstractmethod
    def get_model(self):
        pass

    @abstractmethod
    def cluster(self):
        pass

    @abstractmethod
    def update_view(self):
        pass
    
class WholeSignalClusteringControler(AbstractClusteringControler):
    def __init__(self, content: ClusteringPageContent):
        super().__init__(content)
        
    def get_model(self) -> AbstractModel:
        model = model_factory(
            name="new_model",
            method= self.content.clustering_settings_section.clustering_alogorithm_selector.value,
            f_sampling=self.content.select_files_section.frequency_entry.value,
            n_maps=4,
            path=None
        )

    

