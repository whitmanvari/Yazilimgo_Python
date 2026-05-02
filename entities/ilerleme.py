#ilerleme durumu dataclassı

from datetime import datetime
from entities.base import Base
from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

#C#taki onModelCreating methodunun karşılığı Python'da __table_args__
class IlerlemeKaydi(Base):
    __tablename__ = "ilerleme_durumu"
    __table_args__ = (
        CheckConstraint("durum IN ('tamamlandi', 'devam_ediyor', 'kilitli')", name="ck_durum"),
        UniqueConstraint("kullanici_id", "ders_id", name="uq_kullanici_ders"),
    )
    #check constraint, enum gibi çalışır. Unique constraint sütunun içeriği ile ilgilenmez, yalnızca aynı kombinasyon ikinci kez veritabanına giremez kuralını işletmektedir. 
    #Bu sayede örneğin Hazal, Ders 5 için yalnızca bir kez kayıt oluşacaktır. İkinci kez aynı kullanıcı ve ders kombinasyonu eklenmeye çalışıldığında veritabanı hata verecektir.

    ilerleme_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    kullanici_id: Mapped[int] = mapped_column(Integer, ForeignKey("kullanicilar.kullanici_id"), nullable=False)
    ders_id: Mapped[int] = mapped_column(Integer, ForeignKey("dersler.ders_id"), nullable=False)
    durum: Mapped[str] = mapped_column(String(20), default="kilitli")  # tamamlandi, devam_ediyor, kilitli
    deneme_sayisi: Mapped[int] = mapped_column(Integer, default=0)
    kazanilan_xp: Mapped[int] = mapped_column(Integer, default=0)
    tamamlanma_tarihi: Mapped[datetime| None] = mapped_column(DateTime, nullable=True)
    sure_saniye: Mapped[int|None] = mapped_column(Integer, nullable=True)  # Kullanıcının dersi tamamlama süresi (saniye cinsinden)

    kullanici: Mapped["Kullanici"] = relationship(back_populates="ilerlemeler")
    ders: Mapped["Ders"] = relationship(back_populates="ilerlemeler")
