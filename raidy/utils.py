from abc import ABC, abstractmethod
import random

class BaseUtil(ABC):

    @abstractmethod
    def info(self):
        """
    Статический метод возвращающий информацию о утилите
    не трогая __str__ и __repr__.
        """
        pass

class MessagesUtil(BaseUtil):

    def __init__(self, text, symbols):
        self.text = text
        self.symbols = symbols

    @staticmethod
    def generate_random_id():
        """
    Статический метод возвращающий
    random_id для отправки сообщения.
        """
        return random.randint(0, 1000000)


    def mask_message(self):
        """
    Базовая маска для сообщений
    возвращающая сообщение + рандомное число.
        """
        return self.text + ' ' + str(random.randint(1, 10000000))

    def trimming_message(self):
        """
    Обрезка начала сообщения по переданному
    количеству символов + рандомное число от 1
    до 3-х.
        """
        symbols = [x+random.randint(1, 3) for x in range(self.symbols)]
        symbol = random.choice(symbols)
        return self.text[symbol:]

    @staticmethod
    def info():
        information = "Утилита для упрощения работы с отправляемыми сообщениями"
        return information

    def __str__(self):
        return "text: {} ; symbols: {}".format(self.text, self.symbols)
