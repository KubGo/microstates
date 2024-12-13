from abc import ABC
from gui.main_contents.interfaces import AbstractMainContent

class AbstractController(ABC):

    def __init__(self, content: AbstractMainContent):
        super().__init__()

    