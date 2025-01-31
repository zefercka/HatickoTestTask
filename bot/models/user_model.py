from sqlalchemy.orm import Mapped, mapped_column

from ..dependecies.database import Base

class User(Base):
    __tablename__ = "users"
    
    user_id: Mapped[int] = mapped_column(primary_key=True)
    level_permission: Mapped[int] = mapped_column(nullable=False, default=1)
    token: Mapped[str] = mapped_column(unique=True, nullable=True)