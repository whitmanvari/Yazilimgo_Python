from dal.database import DatabaseManager
from dal.kullanici_repository import KullaniciRepository
from bll.analytics_engine import AnalyticsEngine

def main():
    db = DatabaseManager()
    session = db.get_session()
    
    kullanici_repo = KullaniciRepository(session)
    analiz_motoru = AnalyticsEngine(kullanici_repo)

    print("explode testi")
    
    aranan_ogrenci = "Ahmett"
    print(f"\n {aranan_ogrenci} için özel pasta grafiği oluşturuluyor...")
    analiz_motoru.kisiye_ozel_seviye_dagilimi_ciz(aranan_ogrenci)

if __name__ == "__main__":
    main()