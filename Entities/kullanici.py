from datetime import datetime, date
from entities.base import Base
from sqlalchemy import Integer, String, Date, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship 


class Kullanici(Base):
    __tablename__ = "kullanicilar"

    kullanici_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement= True)
    kullanici_adi: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    parola_hash: Mapped[str] = mapped_column(String(256), nullable=False)
    toplam_xp: Mapped[int] = mapped_column(Integer, default=0 )
    seviye: Mapped[int] = mapped_column(Integer, default=1)
    gunluk_hedef_xp: Mapped[int] = mapped_column(Integer, default=20)
    gun_serisi: Mapped[int] = mapped_column(Integer, default=0)
    son_aktif_tarihi: Mapped[date | None] = mapped_column(Date, nullable=True)
    kayit_tarihi: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    avatar_yolu: Mapped[str| None] = mapped_column(String(255), nullable=True)

    # İlişkiler
    ilerlemeler: Mapped[list["IlerlemeKaydi"]] = relationship(back_populates="kullanici", cascade="all, delete-orphan") 
    kazanimlar:   Mapped[list["KullaniciKazanim"]] = relationship(back_populates="kullanici", cascade="all, delete-orphan")

    #c#taki toString() metodunu ezmeye benzer bir şekilde, kullanıcı nesnesinin okunabilir bir temsilini sağlar.
    def _repr__(self) -> str:
        return f"<Kullanici {self.kullanici_adi} | Seviye {self.seviye}>"
     #kullanılan <> işareti tamamen görsel bir tercih. Best Practise'ler arasında, "Veritabanı Objesi / Sınıf Temsili" olduğunu ilk bakışta anlamak için geleneksel olarak bu ok işaretlerini kullanırlar.
