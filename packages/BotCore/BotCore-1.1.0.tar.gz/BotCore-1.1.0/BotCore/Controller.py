
from BotCore.Bot import Bot
from BotCore.Handlers import register_handlers


class Controller:

	def __init__(self, bot: Bot):
		self.bot = bot
		register_handlers(self)
