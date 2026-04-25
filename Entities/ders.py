#ders dataclassı

from sqlalchemy import CheckConstraint, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from Yazilimgo_Python.entities.modul import DersModulu
from entities.base import Base

#c# karşılığı enum 
DERS_TURLERI = ("coktan_secmeli", "bosluk_doldurma", "kod_yazma", "eslestirme")

class Ders(Base):
    __tablename__ = "dersler"
    __table_args__ = (
        CheckConstraint(f"ders_turu IN {DERS_TURLERI}", name="ck_ders_turu"),
    )

    ders_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    modul_id: Mapped[int] = mapped_column(Integer, ForeignKey("ders_modulleri.modul_id"), nullable=False)
    ders_basligi: Mapped[str] = mapped_column(String(100), nullable=False)
    ders_turu: Mapped[str] = mapped_column(String(30), nullable=False)
    soru_metni: Mapped[str] = mapped_column(Text, nullable=False) #nvarchar(max) karşılığı
    kod_sablonu: Mapped[str | None] = mapped_column(Text, nullable=True)   # kod_yazma türü için
    dogru_cevap: Mapped[str] = mapped_column(Text, nullable=False)  # JSON string, sebebi: çoktan seçmeli, boşluk doldurma, eşleştirme gibi char, list veya dict yapıları içerebilir
    ipucu: Mapped[str | None] = mapped_column(String(500), nullable=True)
    kazanilan_xp: Mapped[int] = mapped_column(Integer, default=10)
    sira_no: Mapped[int] = mapped_column(Integer, nullable=False)

    # Many-to-One: her ders bir modüle ait
    modul: Mapped["DersModulu"] = relationship(back_populates="dersler")

    # One-to-Many: ilerleme kayıtları
    ilerlemeler: Mapped[list["IlerlemeKaydi"]] = relationship(back_populates="ders", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Ders {self.ders_basligi} | {self.ders_turu}>"
    