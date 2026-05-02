from dal.database import DatabaseManager
from dal.kullanici_repository import KullaniciRepository
from bll.kullanici_servisi import KullaniciServisi
from seed import seed_verileri_yukle

def main():
    db = DatabaseManager()
    db.init_db()  # Veritabanı tablolarını oluştur

    seed_verileri_yukle()  

    session = db.get_session()
    repo = KullaniciRepository(session)
    servis = KullaniciServisi(repo)

    print("İş katmanı testi: ")
    #kısa şifre senaryosu
    servis.kayit_ol(kullanici_adi="Ahmett", email="ahmett@ornek.com", sifre="123")
    #uzun şifre ile yine denerse
    yeni_kullanici = servis.kayit_ol(kullanici_adi="Ahmett", email="ahmett@ornek.com", sifre="123456")
    if yeni_kullanici:
        print(f"Süper yeni kullanici {yeni_kullanici.kullanici_adi} kaydedildi.")
        izin1=servis.giris_yap(kullanici_id=yeni_kullanici.kullanici_id, girilen_sifre="YanlisSifre")
        print(f"İzin verdi mi: {izin1}")
        #doğru şifre senaryosu
        izin2=servis.giris_yap(kullanici_id=yeni_kullanici.kullanici_id, girilen_sifre="123456")
        print(f"İzin 2 oldu mu? {izin2}")
    else:
        print("Kullanıcı eklenemedi..")
if __name__ == "__main__":
    main()