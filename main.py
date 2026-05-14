from dal.database import DatabaseManager
from dal.kullanici_repository import KullaniciRepository
from dal.kazanim_repository import KazanimRepository
from bll.kazanim_servisi import KazanimServisi
from seed import seed_verileri_yukle


def main():
    db = DatabaseManager()
    db.init_db()  # Veritabanı tablolarını oluştur

    seed_verileri_yukle()  

    session = db.get_session()
    repo = KullaniciRepository(session)
    kazanim_repo=KazanimRepository(session)
    kazanim_servisi=KazanimServisi(kazanim_repo)

    print("Kazanım testi: ")
    
    kullanicilar = repo.tum_kullanicilari_getir()
    test_kullanici = next((k for k in kullanicilar if k.kullanici_adi == "Ahmett"), None)                 
    
    if test_kullanici:
        print(F"Mevcut Durum: {test_kullanici.kullanici_adi} | Seviye: {test_kullanici.seviye}")

        print("Deneme")
        kazanim_servisi.rozet_ver(kullanici_id=test_kullanici.kullanici_id, kazanim_id=1)
        print("Aynı rozeti verirsek ifimiz çalışıyor mu bakalım")
        kazanim_servisi.rozet_ver(kullanici_id=test_kullanici.kullanici_id, kazanim_id=1)

    else:
        print(f"{test_kullanici.kullanici_adi} kullanıcısı veritabanında yok!")

if __name__ == "__main__":
    main()