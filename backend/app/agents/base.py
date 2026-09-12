from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAgent(ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        '''Every agent must implement this method to process a task.'''
        pass
