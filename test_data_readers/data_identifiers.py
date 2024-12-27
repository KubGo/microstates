from abc import ABC, abstractmethod

class AbstractDataIdentifier(ABC):
    """Interface for data identifiers
    Helps to sort data by its ID and activity 
    """

    def __init__(self):
        super().__init__()

    @abstractmethod
    def get_id(self, file_name: str) -> str:
        """Gets identifier of the file

        Args:
            file_name (str): File name

        Returns:
            str: Identifier of the file
        """
        pass
    
    @abstractmethod
    def get_activity(self, file_name: str) -> str:
        """Gets activity of the file

        Args:
            file_name (str): File name

        Returns:
            str: Avtivity of the file
        """
        pass

class FilePathDataIdentifier(AbstractDataIdentifier):
    """Identify the data by its file name, activity not specified"""
    def __init__(self):
        super().__init__()
        
    def get_id(self, file_name: str):
        return file_name
    
    def get_activity(self, file_name: str):
        return "Not specified"
    
class DelimiteredDataIdentifier(AbstractDataIdentifier):
    """Identify data by its file name parts that are separated by delimiter.
    like: XX_YY_ZZ with id_position = 1 -> XX, activity_position = 3 -> ZZ
    """
    def __init__(self, delimiter: str, id_position: int, activity_position: int):
        super().__init__()
        self.delimiter = delimiter
        self.id_position = id_position
        self.activity_position = activity_position

    def get_id(self, file_name: str):
        return file_name.split(self.delimiter)[self.id_position]
    
    def get_activity(self, file_name: str):
        return file_name.split(self.delimiter)[self.activity_position]