from aiovk import API, TokenSession
from aiovk.longpoll import BotsLongPoll
from abc import ABC, abstractmethod
from exceptions import *
from logsys import Log
from utils import mask_message, trimming_message
import keyboard
import asyncio

"""
:authors: prostomarkeloff, crinny, triedgrief

"""



class BaseRaid(ABC):

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def _check_group(self):
        pass

    @abstractmethod
    def _enable_longpoll():
        pass


class FullRaid(BaseRaid):

    def __init__(self, token, group_id, message_raid, symbols, send_keyboard=False, keyboard_text="Raidy perfect.."):
        """
        :param token: Токен паблика ВКонтакте
        :param group_id: ID паблика ВКонтакте
        :param message_raid: Сообщение для рейда
        :param symbols: Количество символов для обрезки сообщения
                (см. utils.py -> trimming_message)
        :param send_keyboard: Отправление клавиатуры
        :param keyboard_text: Текст для клавиатуры (если не указан, то
                по умолчанию будет использоватся <<Raidy perfect...>>)
        """
        self.token = token
        self.group_id = group_id
        self.message_raid = message_raid
        self.symbols = symbols if symbols > 2 else 5
        self.send_keyboard = send_keyboard
        self.keyboard_text = keyboard_text

        self.session = TokenSession(access_token=self.token) # vk session object
        self.api = API(self.session) # API object
        self.lp = BotsLongPoll(self.api, mode=2, group_id=self.group_id) # longpoll object

        self.logger = Log("raid_log")

    async def _check_group(self):
        """
        Проверка настроек LongPoll сервера паблика.
        Возвращает True если LongPoll сервер включен + необходимые события
        включены. В противном случае - включает их сам и вовзращает True.
        """
        response = await self.api.groups.getLongPollSettings(group_id=self.group_id)
        longpoll_enabled = response["is_enabled"]
        if longpoll_enabled:
            events = response["events"]
            if events["message_new"]:
                return True

            await self._enable_longpoll(self.api, self.group_id)
            return True

        await self._enable_longpoll(self.api, self.group_id)
        return True

    async def run(self):

        """
        Запуск бота + проверка группы.
        """
        self.logger.info("Succesfully started.")
        await self._check_group()
        await self._run()


    async def _run(self):
        """
        Тут сама прослушка.
        """
        # TODO: сделайте это... плиз..

    @staticmethod
    async def _enable_longpoll(api, group_id):
        """
        :param api: Объект API
        :param group_id: ID паблика ВКонтакте

        Включает LongPoll в сообществе + включает событие message_new

        Возвращает True если операция завершена с успехом.
        """

        await api.groups.setLongPollSettings(group_id=group_id, enabled=1, message_new=1)
        return True

    @staticmethod
    async def _create_keyboard(text):
        """
        Создаёт JSON клавиатуры с указаным текстом и возвращает его.
        """
        pass
        # TODO: сделайте это. пожалуйста(
