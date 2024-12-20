from .interfaces import AbstractController
from gui.main_contents.reports_page import ReportsPage
from gui.results_observers import AbstractResultsObserver, CurrentSessionResults


class ReportsController(AbstractController, AbstractResultsObserver):
    def __init__(self, view: ReportsPage):
         self.view = view

    def results_update(self):
        results_info = self.current_session_results.results[-1]
        self.view.session_results.add_result(results_info.results_name)