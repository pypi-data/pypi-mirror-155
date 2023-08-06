
from typing import TypeVar, Generic, Type

from BotCore import DAO
from BotCore.ModelInfo import ModelInfo

T = TypeVar("T", bound=ModelInfo)


class Service(Generic[T]):

	def __init__(self, model: Type[T], dao: DAO[T]):
		self.model = model
		self.dao = dao

	def create(self, **kwargs):
		return self.dao.create(**kwargs)

	def delete(self, row_id):
		return self.dao.delete(row_id)

	def getall(self):
		return self.dao.getall()

	def to_objects(self, rows: list[tuple]) -> list[T]:
		return [self.to_object(row) for row in rows]

	def to_object(self, row: tuple) -> T:
		return self.model(dict(zip(self.model.fields(), row)))
