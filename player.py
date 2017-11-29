from abc import ABC, abstractmethod

class Player(ABC):

    @abstractmethod
    def play_move(self, state):
        message = 'Player subclass must define play_move'
        raise NotImplementedError(message)
