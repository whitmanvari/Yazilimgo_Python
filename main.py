from dal.database import DatabaseManager
from dal.kullanici_repository import KullaniciRepository
from bll.kullanici_servisi import KullaniciServisi
from seed import seed_verileri_yukle
from entities.modul import DersModulu

def main():
    db = DatabaseManager()
    db.init_db()  # Veritabanı tablolarını oluştur

    seed_verileri_yukle()  

    session = db.get_session()
    repo = KullaniciRepository(session)
    servis = KullaniciServisi(repo)

    print("İş katmanı testi başlıyor..")

    servis.kayit_ol(kullanici_adi="Ahmet", email="ahmet@ornek.com", sifre="123")
if __name__ == "__main__":
    main()