from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped

from core.models.base import Base


class TelegramClient(Base):
    __tablename__: str = 'b_crm_t_telegram_clients'
    __table_args__ = {'schema': 'public'}

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    customer_id: Mapped[int] = Column(Integer, primary_key=True, unique=True)
    telegram_id: Mapped[int] = Column(Integer, primary_key=True, unique=True)
    data_hash: Mapped[str] = Column(String(255))

