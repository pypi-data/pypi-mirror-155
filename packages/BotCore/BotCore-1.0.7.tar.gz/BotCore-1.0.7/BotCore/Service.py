
from typing import TypeVar, Generic, Type

from BotCore.ModelInfo import ModelInfo

T = TypeVar("T", bound=ModelInfo)


class Service(Generic[T]):

	def __init__(self, model: Type[T]):
		self.model = model

	def to_objects(self, rows: list[tuple]) -> list[T]:
		return [self.to_object(row) for row in rows]

	def to_object(self, row: tuple) -> T:
		return self.model(dict(zip(self.model.fields(), row)))
