from .base import Base
from sqlalchemy import UniqueConstraint, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

class KullaniciKazanim(Base):
    __tablename__ = "kullanici_kazanimlari"
    __table_args__ = (
        UniqueConstraint("kullanici_id", "kazanim_id", name="uq_kullanici_kazanim"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    kullanici_id: Mapped[int] = mapped_column(Integer, ForeignKey("kullanicilar.kullanici_id"), nullable=False)
    kazanim_id: Mapped[int] = mapped_column(Integer, ForeignKey("kazanim_tanimi.kazanim_id"), nullable=False)
    kazanilma_tarih: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    kullanici: Mapped["Kullanici"] = relationship(back_populates="kazanimlar")
    kazanim_tanimi: Mapped["KazanimTanimi"] = relationship(back_populates="kullanici_kazanimlari")