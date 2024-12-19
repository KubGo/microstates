from abc import ABC, abstractmethod
from gui.main_contents.reports_page import ReportsPage
from gui.controllers.interfaces import AbstractController

class AbstractResultsObserver(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def results_update(self):
        pass

class CurrentSessionResultsObserver(AbstractResultsObserver):
    def __init__(self, results_page: ReportsPage):
        self.results_page = results_page

    def results_update(self):
        pass

class ResultsUpdatesPublisher:
    def __init__(self):
        self.observers: list[AbstractResultsObserver] = []
        
    def register(self, observer: AbstractResultsObserver):
        self.observers.append(observer)

    def update(self):
        for observer in self.observers:
            observer.results_update()

class CurrentSessionResults:
    def __init__(self, controllers: list[AbstractController]):
        self.results_paths = []
        self.observers: list[AbstractResultsObserver] = []
        for controller in controllers:
            controller.current_session_results = self
            self.register(controller)
        self.observers: list[AbstractResultsObserver] = []

    def register(self, observer: AbstractResultsObserver):
        self.observers.append(observer)

    def update(self):
        for observer in self.observers:
            observer.results_update()
