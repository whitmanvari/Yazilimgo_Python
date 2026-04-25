#kazanım + kazanım tanıtımı dataclassı

from datetime import datetime
from sqlalchemy import CheckConstraint, Integer, String, DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from entities.base import Base


KOSUL_TURLERI = ("xp_esigi","ders_sayisi","gun_serisi","ilk_ders","modul_tamamla")

class KazanimTanimi(Base):
    __tablename__ = "kazanim_tanimi"
    __table_args__ = (
        CheckConstraint(f"kosul_turu IN {KOSUL_TURLERI}", name="ck_kosul_turu"),
    )

    kazanim_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    kazanim_adi: Mapped[str] = mapped_column(String(100), nullable=False)
    aciklama: Mapped[str|None] = mapped_column(String(500), nullable=True)
    ikon_adi: Mapped[str|None] = mapped_column(String(50), nullable=True)
    kosul_turu: Mapped[str] = mapped_column(String(30), nullable=False)
    kosul_degeri: Mapped[int] = mapped_column(Integer, nullable=False)

    kullanici_kazanimlari: Mapped[list["KullaniciKazanim"]] = relationship(back_populates="kazanim_tanimi", cascade="all, delete-orphan")
