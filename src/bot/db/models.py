from sqlalchemy import Column, String, Integer, Enum, ForeignKey, TIMESTAMP, Float, TIME
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .enums import RoleType, DaysOfWeek, SmileType
from .main import Database


class User(Database.BASE):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True)
	telegram_id = Column(Integer, nullable=False, unique=True, index=True)
	telegram_name = Column(String(100), nullable=False)
	role = Column(Enum(RoleType, name='role'), nullable=False)
	user_class = Column(String(5), nullable=False, index=True)
	create_at = Column(TIMESTAMP, server_default=func.now())

	extra_lessons = relationship("ExtraLesson", back_populates="user")
	progresses = relationship("Progres", back_populates="user")

	def __repr__(self):
		return f"User({self.id=}, {self.telegram_id=}, {self.telegram_name=} {self.role=}, {self.user_class=}, {self.create_at=})"


class ExtraLesson(Database.BASE):
	__tablename__ = "extra_lessons"

	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
	title = Column(String(100), nullable=False)
	day = Column(Enum(DaysOfWeek, name="day"), nullable=False, index=True)
	time_start = Column(TIME, nullable=False)
	time_end = Column(TIME, nullable=False)

	user = relationship("User", back_populates="extra_lessons")

	def __repr__(self):
		return f"ExtraLesson({self.id=}, {self.user_id=}, {self.title=}, {self.day=}, {self.time_start=}, {self.time_end=})"


class Progres(Database.BASE):
	__tablename__ = "progress"

	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
	title = Column(String(100), nullable=False)
	smile = Column(Enum(SmileType, name="smile"), nullable=False)
	experience = Column(Float, nullable=False, default=0)

	user = relationship("User", back_populates="progresses")

	def __repr__(self):
		return f"Progres({self.id=}, {self.user_id=}, {self.title=}, {self.smile=}, {self.experience=})"


def register_models():
	Database.BASE.metadata.create_all(Database().engine)
