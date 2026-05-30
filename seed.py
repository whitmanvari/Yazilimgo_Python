from dal.database import DatabaseManager
from entities.modul import DersModulu
from entities.ders import Ders
from entities.kazanim import KazanimTanimi
from entities.kullanici import Kullanici

def seed_verileri_yukle():
    db = DatabaseManager()
    db.init_db()
    session = db.get_session()

    if session.query(Kullanici).first() is None:
        k1 = Kullanici(kullanici_adi="Hazal", email="hazal@marmara.edu.tr", parola_hash="1234")
        k2 = Kullanici(kullanici_adi="Ahmet", email="ahmet@network.com", parola_hash="1234")
        k3 = Kullanici(kullanici_adi="Tahsin", email="tahsin@gmail.com", parola_hash="1234")
        k4 = Kullanici(kullanici_adi="Abdullah", email="abdullah@gmail.com", parola_hash="1234")
        session.add_all([k1, k2, k3, k4])
        session.commit()

    if session.query(DersModulu).first() is None:
        modul1 = DersModulu(modul_adi="Python Temelleri", aciklama="Programlamaya giriş yapıyoruz.", dil="Python", sira_no=1)
        modul2 = DersModulu(modul_adi="Veritabanı Mantığı", aciklama="SQLite ve Python Entegrasyonu.", dil="SQL", sira_no=2)
        session.add_all([modul1, modul2])
        session.commit()

        ders1 = Ders(modul_id=modul1.modul_id, ders_basligi="1. Değişkenler ve Veri Tipleri", ders_turu="kod_yazma", soru_metni="Görev: Ekrana print() fonksiyonu ile 'int' yazdırın.", dogru_cevap="int", kazanilan_xp=10, sira_no=1)
        ders2 = Ders(modul_id=modul1.modul_id, ders_basligi="2. Döngülere Giriş", ders_turu="kod_yazma", soru_metni="Görev: Ekrana print() ile 'merhaba' yazdırın.", dogru_cevap="merhaba", kazanilan_xp=20, sira_no=2)
        ders3 = Ders(modul_id=modul1.modul_id, ders_basligi="3. Fonksiyonlar", ders_turu="kod_yazma", soru_metni="Görev: Ekrana 'def' anahtar kelimesini yazdırın.", dogru_cevap="def", kazanilan_xp=30, sira_no=3)
        ders4 = Ders(modul_id=modul2.modul_id, ders_basligi="1. Select Sorgusu", ders_turu="kod_yazma", soru_metni="Görev: Ekrana 'SELECT' anahtar kelimesini yazdırın.", dogru_cevap="SELECT", kazanilan_xp=50, sira_no=1)

        session.add_all([ders1, ders2, ders3, ders4])
        session.commit()

    if session.query(KazanimTanimi).first() is None:
        rozet1 = KazanimTanimi(kazanim_adi="İlk Kan", aciklama="İlk dersini başarıyla tamamladın!", ikon_adi="ilk_kan", kosul_turu="ilk_ders", kosul_degeri=1)
        rozet2 = KazanimTanimi(kazanim_adi="Döngü Ustası", aciklama="Döngüler konusunda pratik yaptın.", ikon_adi="dongu", kosul_turu="ders_sayisi", kosul_degeri=5)
        rozet3 = KazanimTanimi(kazanim_adi="Hata Avcısı", aciklama="Sistemi hiç çökertmeden kodu çalıştırdın.", ikon_adi="hata", kosul_turu="gun_serisi", kosul_degeri=3)
        rozet4 = KazanimTanimi(kazanim_adi="Veri Bükücü", aciklama="SQL Modülüne başarıyla giriş yaptın.", ikon_adi="sql", kosul_turu="xp_esigi", kosul_degeri=200)
        
        session.add_all([rozet1, rozet2, rozet3, rozet4])
        session.commit()

    print("Tüm kullanıcılar, dersler ve rozetler başarıyla yüklendi!")

if __name__ == "__main__":
    seed_verileri_yukle()