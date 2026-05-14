from dal.database import DatabaseManager
from dal.ders_repository import DersRepository
from bll.ders_servisi import DersServisi

def main():
    db = DatabaseManager()
    session = db.get_session()
    
    ders_repo = DersRepository(session)
    ders_servisi = DersServisi(ders_repo)

    print("Ders servisi testi: ")
    
    test_ders_id = 1
    ders = ders_servisi.ders_icerigi_getir(test_ders_id)

    if ders:
        print(f"Ders Bulundu: {ders.ders_basligi}")
        
        yanlis_deneme = ders_servisi.cevap_dogrula(test_ders_id, "rastgele yanlis bir cevap")
        print(f"Yanlış cevap testi sonucu: {yanlis_deneme}")
        
        dogru_deneme = ders_servisi.cevap_dogrula(test_ders_id, ders.dogru_cevap)
        print(f"Doğru cevap testi sonucu: {dogru_deneme}")
    else:
        print("Veritabanında ders bulunamadı.")

if __name__ == "__main__":
    main()