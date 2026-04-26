#kullanıcı crud işlemleri
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from entities.kullanici import Kullanici

class KullaniciRepository:
    def __init__(self, session: Session):
        # C#'taki Dependency Injection (Constructor Injection) mantığı
        self.session = session

    def kullanici_ekle(self, kullanici_adi: str, email: str, parola_hash: str) -> Kullanici | None:
        """Yeni bir kullanıcıyı veritabanına ekler (C#'taki Add metodu)"""
        yeni_kullanici = Kullanici(
            kullanici_adi=kullanici_adi,
            email=email,
            parola_hash=parola_hash
        )
        
        try:
            self.session.add(yeni_kullanici)  # Masaya koy (UoW)
            self.session.commit()             # Veritabanına kaydet (SaveChanges)
            self.session.refresh(yeni_kullanici) # Veritabanından oluşan ID'yi geri al
            return yeni_kullanici
        except IntegrityError:
            self.session.rollback() # Hata çıkarsa işlemi iptal et
            print("Hata: Bu e-posta veya kullanıcı adı zaten kullanımda!")
            return None

    def id_ile_getir(self, kullanici_id: int) -> Kullanici | None:
        """ID'ye göre kullanıcı bulur (C#'taki Find veya FirstOrDefault metodu)"""
        return self.session.query(Kullanici).filter(Kullanici.kullanici_id == kullanici_id).first()

    def tum_kullanicilari_getir(self) -> list[Kullanici]:
        """Tüm kullanıcıları listeler (C#'taki ToList metodu)"""
        return self.session.query(Kullanici).all()