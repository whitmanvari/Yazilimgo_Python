#ders dataclassı

from sqlalchemy import CheckConstraint, ForeignKey, Integer, String, Text #sütun tiplerim 
from sqlalchemy.orm import Mapped, mapped_column, relationship #sqlalchemy 2.0 ile gelen modern tip ipuçları tabanlı haritalama araçları, bu sayede sütunlarımı oluşturuyorum

from entities.modul import DersModulu
from entities.base import Base

#c# karşılığı enum (tuple kullandım, enum yapısı yerine pythonda hafızada hafif yer tutan ve in sorgularına oturan bir tuple kullandım)
DERS_TURLERI = ("coktan_secmeli", "bosluk_doldurma", "kod_yazma", "eslestirme")

class Ders(Base):
    __tablename__ = "dersler" #veritabanında tablonun adı bu olsun, bellekteki adı ise "Ders"
    __table_args__ = (
        CheckConstraint(f"ders_turu IN {DERS_TURLERI}", name="ck_ders_turu"),
    )
    #table args ve checkconstraint güvenlik önlemi. Uygulama seviyesinde hata yapılsa bile, veritabanında ders_turu olarak deneme gibi bir metin gönderirse sqlite bu kaydı reddeder. 

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

    # Many-to-One: her ders bir modüle ait. Bir modulün içerisinde çok ders olabilir.
    modul: Mapped["DersModulu"] = relationship(back_populates="dersler")

    # One-to-Many: ilerleme kayıtları. Bir dersi birden fazla öğrenci çözebilir. 
    ilerlemeler: Mapped[list["IlerlemeKaydi"]] = relationship(back_populates="ders", cascade="all, delete-orphan")


    #dunder metot---> __repr__ python'a özel dunder metottur. bir ders nesnesini terminale print(ders) şeklinde yazdırdığımızda memory reference'ı çıkması yerine okunabilir <Ders Değişkenler | kod_yazma> çıkmasını sağlar. Debugginge destek olsun diye yazdım. 
    def __repr__(self) -> str:
        return f"<Ders {self.ders_basligi} | {self.ders_turu}>"
    