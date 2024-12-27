from abc import ABC, abstractmethod
from gui.controllers.interfaces import AbstractController
from clustering.results import Results
import flet as ft

class AbstractResultsObserver(ABC):
    def __init__(self):
        self.current_session_results: CurrentSessionResults = None

    @abstractmethod
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
    def __init__(self,page:ft.Page,  controllers: list[AbstractController]):
        self.page = page
        self.results: list[ResultsInfo] = []
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
        self.page.update()

    def add_new_current_session_result(self, results: Results):
        self.results.append(ResultsInfo(results))

class ResultsInfo:
    def __init__(self, results: Results):
        self.results_name = f"{results.id}-{results.activity}"
        self.results_path = results.pickle_path
