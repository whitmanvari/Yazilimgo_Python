from dal.database import DatabaseManager
from entities.modul import DersModulu
from entities.ders import Ders
from entities.kazanim import KazanimTanimi
from entities.kullanici import Kullanici
import hashlib
from dal.database import DatabaseManager

def seed_verileri_yukle():
    db = DatabaseManager()
    db.init_db()
    session = db.get_session()

    if session.query(Kullanici).first() is None:
        ornek_sifre_hash = hashlib.sha256("1234".encode()).hexdigest()
        k1 = Kullanici(kullanici_adi="Hazal", email="hazal@marmara.edu.tr", parola_hash=ornek_sifre_hash)
        k2 = Kullanici(kullanici_adi="Ahmet", email="ahmet@network.com", parola_hash=ornek_sifre_hash)
        k3 = Kullanici(kullanici_adi="Tahsin", email="tahsin@gmail.com", parola_hash=ornek_sifre_hash)
        k4 = Kullanici(kullanici_adi="Abdullah", email="abdullah@gmail.com", parola_hash=ornek_sifre_hash)
        
        session.add_all([k1, k2, k3, k4])
        session.commit()

    if session.query(DersModulu).first() is None:
        modul1 = DersModulu(modul_adi="Python Temelleri", aciklama="Programlamaya giriş yapıyoruz.", dil="Python", sira_no=1)
        session.add(modul1)
        session.commit()

        # GERÇEKÇİ VE KAPSAMLI PYTHON DERSLERİ
        ders1 = Ders(modul_id=modul1.modul_id, ders_basligi="1. Ekrana Yazdırma", ders_turu="kod_yazma", 
                     soru_metni="Görev: print() fonksiyonunu kullanarak ekrana Merhaba kelimesini yazdırın.", 
                     dogru_cevap="Merhaba", kazanilan_xp=10, sira_no=1)
        
        ders2 = Ders(modul_id=modul1.modul_id, ders_basligi="2. Değişken Tanımlama", ders_turu="kod_yazma", 
                     soru_metni="Görev: x adında bir değişken oluşturun, içine 50 değerini atayın ve ekrana yazdırın", 
                     dogru_cevap="50", kazanilan_xp=20, sira_no=2)
        
        ders3 = Ders(modul_id=modul1.modul_id, ders_basligi="3. Matematiksel İşlemler", ders_turu="kod_yazma", 
                     soru_metni="Görev: 15 ile 25'i toplayıp sonucu print() ile ekrana yazdırın.", 
                     dogru_cevap="40", kazanilan_xp=20, sira_no=3)
        
        ders4 = Ders(modul_id=modul1.modul_id, ders_basligi="4. Metin (String) Birleştirme", ders_turu="kod_yazma", 
                     soru_metni="Görev: ad = 'Yazilim' ve soyad = 'Go' değişkenlerini toplayarak print() ile yazdırın.", 
                     dogru_cevap="YazilimGo", kazanilan_xp=30, sira_no=4)

        ders5 = Ders(modul_id=modul1.modul_id, ders_basligi="5. Listeler (Diziler)", ders_turu="kod_yazma", 
                     soru_metni="Görev: sayilar = [10, 20, 30] listesinin ilk elemanını (0. indeks) ekrana yazdırın.", 
                     dogru_cevap="10", kazanilan_xp=40, sira_no=5)

        ders6 = Ders(modul_id=modul1.modul_id, ders_basligi="6. For Döngüsü", ders_turu="kod_yazma", 
                     soru_metni="Görev: for döngüsü ile 0'dan 2'ye kadar olan sayıları alt alta yazdırın.", 
                     dogru_cevap="0\n1\n2", kazanilan_xp=50, sira_no=6)
                     
        ders7 = Ders(modul_id=modul1.modul_id, ders_basligi="7. Koşullu Durumlar (If-Else)", ders_turu="kod_yazma", 
                     soru_metni="Görev: x = 10 değişkeni 5'ten büyükse ekrana Buyuk yazdırın.", 
                     dogru_cevap="Buyuk", kazanilan_xp=60, sira_no=7)
        ders8 = Ders(modul_id=modul1.modul_id, ders_basligi="8. Ekrana Yazdırma", ders_turu="kod_yazma", 
                     soru_metni="Görev: Ekrana selam yazdırın! ", 
                     dogru_cevap="Selam", kazanilan_xp=10, sira_no=8)
        ders9 = Ders(modul_id=modul1.modul_id, ders_basligi="9. Döngü Oluşturma", ders_turu="kod_yazma", 
                     soru_metni="Görev: While True döngüsü oluşturun ve 3 defa '1' yazdırın.",
                     dogru_cevap="1\n1\n1", kazanilan_xp=60, sira_no=9)

        session.add_all([ders1, ders2, ders3, ders4, ders5, ders6, ders7,ders8,ders9])
        session.commit()

    if session.query(KazanimTanimi).first() is None:
        rozet1 = KazanimTanimi(kazanim_adi="İlk Deneme", aciklama="İlk dersini başarıyla tamamladın!", ikon_adi="ilk_deneme", kosul_turu="ilk_ders", kosul_degeri=1)
        rozet2 = KazanimTanimi(kazanim_adi="Döngü Başarısı", aciklama="Döngüler konusunda pratik yaptın.", ikon_adi="dongu", kosul_turu="ders_sayisi", kosul_degeri=5)
        rozet3 = KazanimTanimi(kazanim_adi="Hata Avcısı", aciklama="Sistemi hiç çökertmeden kodu çalıştırdın.", ikon_adi="hata", kosul_turu="gun_serisi", kosul_degeri=3)
        rozet4 = KazanimTanimi(kazanim_adi="Veri Bükücü", aciklama="SQL Modülüne başarıyla giriş yaptın.", ikon_adi="sql", kosul_turu="xp_esigi", kosul_degeri=200)
        
        session.add_all([rozet1, rozet2, rozet3, rozet4])
        session.commit()

    print("Tüm kullanıcılar, dersler ve rozetler başarıyla yüklendi!")

if __name__ == "__main__":
    seed_verileri_yukle()