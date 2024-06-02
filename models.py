from sqlalchemy import String
from database import Base
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(20), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String)
    api_key: Mapped[str] = mapped_column(String, nullable=True)

    def __repr__(self):
        return f"User(id:{self.id}, username:{self.username})"
