
import os
import time
import sqlite3
from sqlite3 import Connection, Cursor
from typing import Any, Callable


class DataBase:

	conn: Connection = None
	cursor: Cursor = None

	@staticmethod
	def _execute(func: Callable[[str, tuple], Any], query: str, args: tuple = ()) -> Any:
		error = None
		for i in range(3):
			try:
				print(query, args)
				result = func(query, args)
				print(result)
				return result
			except sqlite3.ProgrammingError as e:
				error = e
				time.sleep(1)
		raise Exception(error)

	def __init__(self, dbpath: str, structure_path: str = None):
		self.dbpath = dbpath
		self.structure_path = structure_path
		if not os.path.exists(self.dbpath) and self.structure_path is not None:
			with open(dbpath, "w") as file:
				file.write("")
			self.connect(dbpath)
			self._create_structure()
		else:
			self.connect(dbpath)

	def connect(self, filename: str):
		self.conn = sqlite3.connect(filename, check_same_thread=False)
		self.cursor = self.conn.cursor()
		self.conn.create_function("lower", 1, lambda string: string.lower() if string else None)
		self.conn.create_function("IIF", 3, lambda cond, positive, negative: positive if cond else negative)

	def close(self):
		self.cursor.close()
		self.conn.close()

	def fetchall(self, query: str, *args: Any) -> list[tuple]:
		return self._execute(self._fetchall, query, args=args)

	def fetchone(self, query: str, *args: Any) -> tuple:
		return self._execute(self._fetchone, query, args=args)

	def update(self, query: str, *args: Any) -> Any:
		return self._execute(self._update, query, args=args)

	def _fetchall(self, query: str, args: Any = ()) -> list[tuple]:
		self.cursor.execute(query, args)
		return self.cursor.fetchall()

	def _fetchone(self, query: str, args: Any = ()) -> tuple:
		self.cursor.execute(query, args)
		return self.cursor.fetchone()

	def _update(self, query: str, args: Any = ()) -> Any:
		self.cursor.execute(query, args)
		self.conn.commit()
		return self.cursor.lastrowid

	def _create_structure(self):
		with open(self.structure_path, "r") as structure:
			self.cursor.executescript(structure.read())
