
from abc import ABC, abstractmethod
from typing import Any

class StorageService(ABC):
 
    @abstractmethod
    def save_file(self, file_content:Any, file_name:str, **config) -> None:
         pass

    @abstractmethod
    def download_file(self, path:str, file_name:str, **config) -> None:
         pass

    @abstractmethod
    def getContent_file(self, **config):
        pass 
