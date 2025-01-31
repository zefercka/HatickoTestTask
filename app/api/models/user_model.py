from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from ..dependecies.database import Base

class User(Base):
    __tablename__ = "users"
    
    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(16))
    email: Mapped[str] = mapped_column(String(256))
    password_hash: Mapped[str]
    token: Mapped[str] = mapped_column(unique=True, nullable=True)