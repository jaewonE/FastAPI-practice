from __future__ import annotations
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from db_base import db_base


class UserTable(db_base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    password = Column(String(200), nullable=False)

    # 기본적으로 컬렉션을 자동 로드하지 않음(noload).
    # 필요할 때 쿼리 옵션(selectinload/joinedload)으로 명시적으로 로드.
    # 부모(User) 삭제 시 연관된 Todo도 모두 삭제.
    todos = relationship(
        "TodoTable",
        back_populates="owner",
        cascade="all, delete-orphan",
        lazy="noload",
        passive_deletes=True,
        order_by="TodoTable.id",
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def create(cls, data: dict) -> UserTable:
        return cls(**data)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            # "password": self.password,  # 보안상 제외
        }

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name})>"
