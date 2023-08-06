from typing import Any


class ModelInfo:

	@classmethod
	def table(cls):
		raise NotImplementedError()

	@classmethod
	def fields(cls):
		raise NotImplementedError()

	def __init__(self, data: dict[str, Any]):
		for field in self.fields():
			self.__setattr__(field, data.get(field))
