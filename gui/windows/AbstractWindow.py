import customtkinter
from abc import ABC, abstractmethod
from gui.windows.RefreshTextIntefrace import RefreshTextInterface

class AbstractWindow(customtkinter.CTkFrame, RefreshTextInterface, ABC):
    
    def __init__(self, master):
        super(AbstractWindow, self).__init__(master=master)

    @abstractmethod
    def show(self):
        pass
    
    @abstractmethod
    def hide(self):
        pass 
