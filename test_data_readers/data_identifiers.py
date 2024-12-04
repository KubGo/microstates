from abc import ABC, abstractmethod

class AbstractDataIdentifier(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def get_id(self, file_name: str) -> str:
        pass
    
    @abstractmethod
    def get_activity(self, file_name: str) -> str:
        pass

class FilePathDataIdentifier(AbstractDataIdentifier):
    def __init__(self):
        super().__init__()
        
    def get_id(self, file_name: str):
        return file_name
    
    def get_activity(self, file_name: str):
        return "Not specified"
    
class DelimiteredDataIdentifier(AbstractDataIdentifier):
    def __init__(self, delimiter: str, id_position: int, activity_position: int):
        super().__init__()
        self.delimiter = delimiter
        self.id_position = id_position
        self.activity_position = activity_position

    def get_id(self, file_name: str):
        return file_name.split(self.delimiter)[self.id_position]
    
    def get_activity(self, file_name: str):
        return file_name.split(self.delimiter)[self.activity_position]