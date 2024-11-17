import customtkinter
from abc import ABC, abstractmethod

class AbstractWindow(customtkinter.CTkFrame, ABC):
    
    def __init__(self, master):
        super(AbstractWindow, self).__init__(master=master)
    
    @abstractmethod
    def refresh_text(self, language):
        pass

    @abstractmethod
    def show(self):
        pass
    
    @abstractmethod
    def hide(self):
        pass 
