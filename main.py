from dal.database import DatabaseManager
from dal.kullanici_repository import KullaniciRepository
from seed import seed_verileri_yukle
from entities.modul import DersModulu

def main():
    db = DatabaseManager()
    db.init_db()  # Veritabanı tablolarını oluştur

    seed_verileri_yukle()  

    session = db.get_session()
    kullanici_repo = KullaniciRepository(session)

    print("Yazılımgo başlatıldı!")

    moduller= session.query(DersModulu).all()
    print("Yüklü modüller: "+ str(len(moduller)) + "adet.")
    for modul in moduller:
        print(modul.modul_adi + "-" + "XP Çarpanı:" + str(modul.xp_carpani))

    kullanicilar = kullanici_repo.tum_kullanicilari_getir()
    print("Kayıtlı kullanıcılar " + str(len(kullanicilar)) + " adet.")
    for kullanici in kullanicilar:
        print(kullanici.kullanici_adi + " - " + kullanici.email + " - " + "Seviye: " + str(kullanici.seviye) + " - " + "Toplam XP: " + str(kullanici.toplam_xp))
    
if __name__ == "__main__":
    main()