from abc import ABC, abstractmethod
from ..interfaces import AbstractMainContent
import flet as ft

class AbstractSection(ABC, ft.Row):
    def __init__(self, content_page: AbstractMainContent):
        super(ft.Row, self).__init__()
        self.content_page = content_page


class AbstractFileObserver(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def file_update(self, files):
        pass
    