import flet as ft
from .interfaces import AbstractController
from gui.main_contents.controllers.clustering_controllers import AbstractClusteringControler
from gui.main_contents.controllers.reporting_controllers import ReportsController
from gui.results_observers import ResultsUpdatesPublisher, AbstractResultsObserver
from gui.results_observers import CurrentSessionResults

class MicrostatesAppController(AbstractController):
    def __init__(self, content, clustering_controller:AbstractClusteringControler, reports_controller: ReportsController):
        super().__init__(content)
        self.clustering_controller = clustering_controller
        self.reports_controller = reports_controller
        self.clustering_controller.current_session_results = self.current_session_results
        self.reports_controller.current_session_results = self.current_session_results

        # Current sesion results updates publisher and observers
        self.current_session_results = CurrentSessionResults(
            [
                self.reports_controller,
                self.clustering_controller
            ]
        )
        # Register results observers
        self.current_session_results.register(self.reports_controller)
        