from typing import Any


class ModelInfo:

	@classmethod
	def table(cls):
		raise NotImplementedError()

	@classmethod
	def fields(cls):
		raise NotImplementedError()

	def __init__(self, data: dict[str, Any]):
		self.__dict__.update(data)
