from typing import Any


class ModelInfo:

	@classmethod
	def table(cls):
		raise NotImplemented()

	@classmethod
	def fields(cls):
		raise NotImplemented()

	def __init__(self, data: dict[str, Any]):
		self.__dict__.update(data)
