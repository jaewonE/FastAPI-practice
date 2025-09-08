# model/todo.py
from __future__ import annotations
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from db_base import db_base


class TodoTable(db_base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(String(2000), nullable=True)
    completed = Column(Boolean, default=False)

    # FK: 사용자 테이블과 연결 (삭제 시 CASCADE)
    owner_id = Column(
        Integer,
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    owner = relationship("UserTable", back_populates="todos")

    @classmethod
    def create(self, data: dict) -> TodoTable:
        return self(
            title=data.get("title").strip(),
            description=data.get("description").strip(
            ) if data.get("description") else None,
            completed=1 if data.get("completed") else 0,
            owner_id=data.get("owner_id")
        )

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": bool(self.completed),
        }

    def __repr__(self):
        return f"<Todo(id={self.id}, title={self.title}, completed={self.completed})>"
