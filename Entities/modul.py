# dersmodulu dataclass'

from sqlalchemy import Integer, String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from entities.base import Base


class DersModulu(Base):
    __tablename__ = "ders_modulleri"

    modul_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    modul_adi: Mapped[str] = mapped_column(String(100), nullable=False)
    aciklama: Mapped[str | None] = mapped_column(String(500), nullable=True)
    dil: Mapped[str] = mapped_column(String(30), default="Python")
    zorunlu_onceki: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("ders_modulleri.modul_id"), nullable=True
    )
    sira_no: Mapped[int] = mapped_column(Integer, nullable=False)
    ikon_adi: Mapped[str | None] = mapped_column(String(50), nullable=True)
    xp_carpani: Mapped[float] = mapped_column(Float, default=1.0)
    
    #self-referential: ön koşul modülü
    on_kosul: Mapped["DersModulu | None"] = relationship("DersModulu", remote_side="DersModulu.modul_id")

    # One-to-Many: bir modülün birden fazla dersi var
    dersler: Mapped[list["Ders"]] = relationship(back_populates="modul", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<DersModulu {self.modul_adi}>"