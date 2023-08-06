from typing import Callable

from telebot.types import Message

handlers_count = {}


def define_priority(method):
	parent = method.__qualname__.rsplit(".", 1)[0]
	parent_handlers_count = handlers_count.get(parent, 0)
	handlers_count.update({parent: parent_handlers_count + 1})
	method.__setattr__("__handler_priority", parent_handlers_count + 1)


def register_handlers(controller):
	handlers = sorted([
		controller.__getattribute__(attr_name) for attr_name in dir(controller)
		if "__register_handler" in dir(controller.__getattribute__(attr_name))
	], key=lambda h: h.__getattribute__("__handler_priority"))
	for handler in handlers:
		handler.__getattribute__("__register_handler")(controller.bot, handler)


def message_handler(commands: list[str] = None, regexp: str = None, func: Callable[[Message], bool] = None,
					content_types: list[str] = None, chat_types: list[str] = None, state: str = None, **kwargs):
	def decorator(method):
		define_priority(method)
		method.__setattr__("__register_handler", lambda bot, handler: bot.register_message_handler(
			handler, commands=commands, regexp=regexp, func=func,
			content_types=content_types, chat_types=chat_types, state=state, **kwargs
		))
		return method
	return decorator


def callback_query_handler(func=None, state=None, **kwargs):
	def decorator(method):
		define_priority(method)
		method.__setattr__("__register_handler", lambda bot, handler: bot.register_callback_query_handler(
			handler, func=func, state=state, **kwargs))
		return method
	return decorator
