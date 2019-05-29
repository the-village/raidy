from abc import ABC, abstractmethod
import random

class BaseUtil(ABC):

    @abstractmethod
    def __str__(self):
        pass


class MessagesUtil(BaseUtil):

    def __init__(self, text, symbols):
        self.text = text
        self.symbols = symbols

    @staticmethod
    def generate_random_id():
        return random.randint(0, 1000000)


    def mask_message(self):
        return self.text + ' ' + str(random.randint(1, 10000000))

    def trimming_message(self):
        symbols = [x+random.randint(1, 3) for x in range(self.symbols)]
        symbol = random.choice(symbols)
        return self.text[symbol:]

    def __str__(self):
        return "text: {} ; symbols: {}".format(self.text, self.symbols)
