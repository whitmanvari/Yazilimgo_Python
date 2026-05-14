from datetime import date, timedelta
from dal.database import DatabaseManager
from dal.kullanici_repository import KullaniciRepository
from bll.streak_servisi import StreakServisi

def main():
    db = DatabaseManager()
    session = db.get_session()
    
    # Sınıfları başlatalım
    kullanici_repo = KullaniciRepository(session)
    streak_servisi = StreakServisi(kullanici_repo)

    print("Streak testi: ")
    
    # Veritabanından Ahmett'i bul
    kullanicilar = kullanici_repo.tum_kullanicilari_getir()
    test_kullanici = next((k for k in kullanicilar if k.kullanici_adi == "Ahmett"), None)

    if test_kullanici:
        print("1: İlk Giriş ")
        # Test için geçmişi temizliyoruz
        test_kullanici.son_aktif_tarihi = None 
        test_kullanici.gun_serisi = 0
        streak_servisi.gunluk_giris_yap(test_kullanici.kullanici_id)
        
        print("2: Aynı Gün İçinde Uygulamayı Tekrar Açma")
        streak_servisi.gunluk_giris_yap(test_kullanici.kullanici_id)
        
        print("3: Ertesi Gün Giriş Yapma ")
        # Dün giriş yapmış gibi tarihi 1 gün geriye alıyoruz
        test_kullanici.son_aktif_tarihi = date.today() - timedelta(days=1)
        streak_servisi.gunluk_giris_yap(test_kullanici.kullanici_id)
        
        print("4: 3 Gün Girmemezlik Yapma (")
        # 3 gün önce giriş yapmış gibi tarihi değiştiriyoruz
        test_kullanici.son_aktif_tarihi= date.today() - timedelta(days=3)
        streak_servisi.gunluk_giris_yap(test_kullanici.kullanici_id)
        
    else:
        print("Kullanıcı veritabanında bulunamadı!")

if __name__ == "__main__":
    main()