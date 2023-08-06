import traceback

from telebot import TeleBot, ExceptionHandler


class Bot(TeleBot, ExceptionHandler):

	def __init__(self, token: str):
		super().__init__(token)
		self.exception_handler = self
		self.init_controllers()

	def init_controllers(self):
		pass

	def start(self):
		self.infinity_polling()

	def stop(self):
		self.stop_bot()

	def handle(self, exception):
		print(traceback.format_exc())
