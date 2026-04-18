#kullanici dataclass'ı
from datetime import datetime, date
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column
from Entities.base import Base 

class Kullanici(Base):
    __tablename__ = "kullanicilar"
    kullanici_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
