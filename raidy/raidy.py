from aiovk import API, TokenSession
from aiovk.longpoll import BotsLongPoll
from abc import ABC, abstractmethod
from exceptions import *
from logsys import Log
from utils import MessagesUtil
from keyboard import VkKeyboard, VkKeyboardColors
import asyncio

"""
:authors: prostomarkeloff, crinny, triedgrief,


"""



class BaseRaid(ABC):
		"""
	Интерфейс для всех производных классов.

		"""

	@abstractmethod
	def run(self):
		"""
	Метод для неявного запуска бота в стороннем файле.
	Как минимум должен содержать вызвов приватного
	метода _check_group и приватного метода
	_run.
		"""
		pass

	@abstractmethod
	def _run(self):
		"""
	Метод для явного запуска бота (получение событий и т.п).
	Должен быть вызван из run.

		"""

	@abstractmethod
	def _check_group(self):
		"""
	Метод для проверки группы на нужные параметры:
	включённый LongPoll, установленные события (чаще всего - message_new).

	По умолчанию должен возвращать True, как сигнал
	о удачном завершении работы.
		"""
		pass

	@abstractmethod
	def _enable_longpoll(self):
		"""
	Метод для включения LongPoll`a в группе и выставления
	нужных событий.

	По умолчанию должен возвращать True, как сигнал
	о удачном завершении работы.
		"""
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
		self.keyboard = self._create_keyboard(text=self.keyboard_text) # keyboard object (json) after generation

		self.session = TokenSession(access_token=self.token) # vk session object
		self.api = API(self.session) # API object
		self.lp = BotsLongPoll(self.api, mode=2, group_id=self.group_id) # longpoll object

		self.logger = Log("raid_log") # logger object. create log file (raid_log.log)

		self.message_util = MessagesUtil(self.text, self.symbols) # MessagesUtil initialization

	async def _check_group(self):
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
		self.logger.info("Succesfully started.")
		await self._check_group()
		await self._run()


	async def _run(self):
		while True:
			data = await self.lp.wait()
			updates = data["updates"]
			print(updates)
			if updates == []:
				continue
			else:
				print(data)
				updates = data["updates"]
				if updates[0]["type"] == "message_new":
					object_updates = updates[0]["object"]
					chat_id = object_updates["peer_id"]
					if "action" in object_updates:
						self.logger.info(f"Start raid in {chat_id}")
						while True:
							message_raid = message_util.mask_message(self.message_raid)
							message_raid = message_util.trimming_message(message_raid, self.symbols)
							try:
								if send_keyboard:
									await self.api.messages.send(message=message_raid, peer_id=chat_id, random_id=0, keyboard=self.keyboard)
								else:
									await self.api.messages.send(message=message_raid, peer_id=chat_id, random_id=0)
							except Exception as e:
								self.logger.exception(e)
								break


	@staticmethod
	async def _enable_longpoll(api, group_id):
		"""
		:param api: Объект API
		:param group_id: ID паблика ВКонтакте
		"""

		await api.groups.setLongPollSettings(group_id=group_id, enabled=1, message_new=1)
		return True

	@staticmethod
	async def _create_keyboard(text):
		"""
		:param text: Текст для кнопок клавиатуры.

		Создаёт JSON клавиатуры с указаным текстом и возвращает его.
		"""
		keyboard = VkKeyboard(one_time=False)
		for x in range(5):
			keyboard.new_button(label=text, color=VkKeyboardColors.NEGATIVE)
			keyboard.new_button(label=text, color=VkKeyboardColors.NEGATIVE)
			keyboard.new_button(label=text, color=VkKeyboardColors.NEGATIVE)
			keyboard.new_line()

		keyboard = keyboard.get_keyboard()
		return keyboard
