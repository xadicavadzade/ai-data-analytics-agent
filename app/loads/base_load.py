from abc import ABC, abstractmethod
from fastapi import UploadFile

class BaseLoader(ABC):

    @abstractmethod
    async def load(self, file: UploadFile) -> str:
        pass