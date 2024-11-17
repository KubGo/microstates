from abc import ABC, abstractmethod

class RefreshTextInterface(ABC):
    
    @abstractmethod
    def refresh_text(self, language: dict):
        pass
    