#matplotlib/numPy grafik motoru 
import matplotlib.pyplot as plt
import numpy as np
from dal.kullanici_repository import KullaniciRepository

class AnalyticsEngine:
    def __init__(self, kullanici_repo: KullaniciRepository):
        self.repo=kullanici_repo
    def xp_liderlik_grafigi_ciz(self):
        kullanicilar = self.repo.tum_kullanicilari_getir()
        if not kullanicilar:
            return

        isimler = [k.kullanici_adi for k in kullanicilar]
        xpler = [k.toplam_xp for k in kullanicilar]

        # Grafik boyutu (10 genişlik, 6 yükseklik)
        plt.figure(figsize=(10,6))
        
        plt.bar(isimler, xpler, color="#630D01")
        
        # Etiketler
        plt.title("YazılımGo - Liderlik Tablosu")
        plt.xlabel("Öğrenciler")
        plt.ylabel("Toplam XP")

        plt.tight_layout() 
        
        # Resmi Kaydet (bbox_inches='tight' demek: "Kenarları kesme, hepsini al" demektir)
        plt.savefig("analiz_liderlik_tablosu.png", bbox_inches='tight')
        plt.close()

    def seviye_dagilimi_ciz(self):
        kullanicilar=self.repo.tum_kullanicilari_getir()
        seviyeler=[k.seviye for k in kullanicilar]

        if not seviyeler:
            return 
        benzersiz_seviyeler, frekanslar= np.unique(seviyeler, return_counts=True)

        plt.figure(figsize=(8,8))
        renkler = ['#ff9999', '#66b3ff', "#ffb17d",'#ffcc99', "#f7ec5c"]

        plt.pie(frekanslar, labels=[f"Seviye {s}" for s in benzersiz_seviyeler],
                autopct='%1.1f%%', startangle=140, colors=renkler, shadow=True)
        
        plt.title("Öğrenci Seviye Dağılımı")

        dosya_adi="analiz_seviye_dagilimi.png"
        plt.savefig(dosya_adi)
        plt.close()

        print(f"Seviye dağılımı grafiği başarıyla çizildi ve {dosya_adi} olarak kaydedildi. ")

    def kisiye_ozel_seviye_dagilimi_ciz(self, hedef_kullanici_adi: str):
        kullanicilar=self.repo.tum_kullanicilari_getir()
        hedef_seviye=None
        for k in kullanicilar:
            if k.kullanici_adi==hedef_kullanici_adi:
                hedef_seviye=k.seviye
                break
        if hedef_seviye is None:
            print("Böyle bir kullanıcı bulunamadı..")
            return 
        seviyeler=[k.seviye for k in kullanicilar]
        benzersiz_seviyeler, frekanslar=np.unique(seviyeler, return_counts=True)

        explode_degerleri=[0.1 if s==hedef_seviye else 0.0 for s in benzersiz_seviyeler]

        plt.figure(figsize=(8,8))
        renkler=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0']

        plt.pie(frekanslar, labels=[f"Seviye {s}" for s in benzersiz_seviyeler],
                autopct='%1.1f%%', colors=renkler, startangle=140,shadow=True, explode=explode_degerleri)
            
        plt.title(f"Öğrenci Seviye Dağılımı (Vurgulanan: {hedef_kullanici_adi})")

        dosya_adi="analiz_hedefli_seviye_dagilimi.png"
        plt.savefig(dosya_adi)
        plt.close()

        print(f"Ön plana çıkarma tamamlandı, {dosya_adi} kaydedildi. ")
            