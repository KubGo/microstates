from abc import ABC, abstractmethod
from . data_identifiers import AbstractDataIdentifier
from . data_read_strategies import AbstractDataReadStrategy
from . data_models import Data
from pathlib import Path

class AbstractDataReader(ABC):

    def __init__(self, 
                data_read_strategy: AbstractDataReadStrategy,
                data_identifier: AbstractDataIdentifier):
        self.data_read_strategy = data_read_strategy
        self.data_identifier = data_identifier
        self.current_position = 0
        self.max_position = 0
        self.data_list: list[Data] = []

    @abstractmethod
    def add_data(self, path: str):
        pass

    @abstractmethod
    def next(self) -> Data:
        pass

    @abstractmethod
    def has_more(self) -> bool:
        pass

class FileDataReader(AbstractDataReader):

    def __init__(self, data_read_strategy, data_identifier):
        super().__init__(data_read_strategy, data_identifier)

    def add_data(self, path):
        signal = self.data_read_strategy.get_data(path)
        file_name = Path(path).stem
        id = self.data_identifier.get_id(file_name)
        activity = self.data_identifier.get_activity(file_name)
        self.data_list.append(
            Data(
                id=id,
                activity=activity,
                data=signal
            )
        )
        self.max_position += 1

    def next(self) -> Data:
        data = self.data_list[self.current_position]
        self.current_position += 1
        return data
        
    def has_more(self) -> bool:
        if self.current_position == self.max_position:
            self.current_position = 0
            return False
        return True

class FolderDataReader(AbstractDataReader):
    def __init__(self, data_read_strategy, data_identifier):
        super().__init__(data_read_strategy, data_identifier)

    def add_data(self, path):
        path = Path(path)
        for file in path.iterdir():
            if file.is_file() and file.suffix == ".csv":
                signal = self.data_read_strategy.get_data(path / file.name)
                file_name = file.stem()
                id = self.data_identifier.get_id(file_name)
                activity = self.data_identifier.get_activity(file_name)
                self.data_list.append(
                    Data(
                        id=id,
                        activity=activity,
                        data=signal
                    )
                )
                self.max_position += 1
        
    def next(self):
        data = self.data_list[self.current_position]
        self.current_position += 1
        
    def has_more(self):
        if self.current_position == self.max_position:
            self.current_position = 0
            return False
        return True
                