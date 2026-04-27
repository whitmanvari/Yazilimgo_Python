from dal.database import DatabaseManager
from entities.modul import DersModulu
from entities.ders import Ders
from entities.kazanim import KazanimTanimi

def seed_verileri_yukle():
    db = DatabaseManager()
    session = db.get_session()  
    if session.query(DersModulu).first is not None:
        print("Veritabanı zaten dolu, seed işlemi atlanıyor.")
        return
    print("Seed verileri yükleniyor...")

    #ilk ders modülü
    modul1=DersModulu(
        modul_adi="Python Temelleri", 
        aciklama="Python programlama dilinin temellerini öğrenin.",
        dil="Python",
        sira_no=1,
        xp_carpani=1.0
    )
    session.add(modul1)
    session.commit() 

    # modüle ait ilk ders
    ders1 = Ders(
        modul_id=modul1.modul_id,
        ders_basligi="Değişkenler ve Veri Tipleri",
        ders_turu="coktan_secmeli",
        soru_metni="Hangi veri tipi sayıları tutar?",
        dogru_cevap='{"cevap": "int"}',
        kazanilan_xp=10,
        sira_no=1
    )
    session.add(ders1)

    kazanim1 = KazanimTanimi(
        kazanim_adi="İlk Adım",
        aciklama="Uygulamada ilk dersini tamamladın!",
        kosul_turu="ilk_ders",
        kosul_degeri=1
    )
    session.add(kazanim1)

    session.commit()
    print("Seed verileri başarıyla yüklendi.")

if __name__ == "__main__":
    seed_verileri_yukle()



        
        