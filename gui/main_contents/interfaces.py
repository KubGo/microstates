from abc import ABC, abstractmethod
from flet import Column, Page

class AbstractMainContent(ABC, Column):

    def __init__(self, page: Page):
        super(Column, self).__init__()
        self.page = page
