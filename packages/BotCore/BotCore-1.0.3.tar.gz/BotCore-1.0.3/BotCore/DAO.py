from typing import Type, TypeVar

from BotCore import DataBase
from BotCore.ModelInfo import ModelInfo

T = TypeVar("T", bound=ModelInfo)


class DAO:

	def __init__(self, database: DataBase, model: Type[T]):
		self.database: DataBase = database
		self.model = model

	def create(self, **kwargs):
		return self.database.update(
			f"INSERT INTO {self.model.table()} ({', '.join(self.model.fields())}) "
			f"VALUES ({', '.join('?' for _ in self.fields())})",
			*[kwargs.get(field) for field in self.fields()]
		)

	def delete(self, row_id):
		return self.database.update(f"DELETE FROM {self.model.table()} WHERE id = ?", row_id)

	def getall(self):
		return self.database.fetchall(f"SELECT {', '.join(self.model.fields())} FROM {self.model.table()}")
