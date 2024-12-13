from abc import ABC, abstractmethod
from main_contents.reports_page import ReportsPage

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

class ResultsObserverPublisher:
    def __init__(self):
        self.observers: list[AbstractResultsObserver] = []
        
    def regiser(self, observer: AbstractResultsObserver):
        self.observers.append(observer)

    def update(self):
        for observer in self.observers:
            observer.results_update()
