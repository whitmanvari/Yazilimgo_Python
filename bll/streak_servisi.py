#günlük seri takibi

from datetime import date, timedelta
from dal.kullanici_repository import KullaniciRepository

class StreakServisi:
    def __init__(self, kullanici_repo: KullaniciRepository):
        self.repo = kullanici_repo

    def gunluk_giris_yap(self, kullanici_id: int):
        kullanici=self.repo.id_ile_getir(kullanici_id)

        if not kullanici:
            print("Hata! Kullanıcı bulunamadı!")
            return None
        bugun=date.today()

        if kullanici.son_aktif_tarihi is None:
            kullanici.gun_serisi=1
            kullanici.son_aktif_tarihi=bugun
            print("1. Gün Tamamlandı!")
        elif kullanici.son_aktif_tarihi == bugun:
            print(f"Bugün zaten giriş yaptın. Mevcut serin devam ediyor. {kullanici.gun_serisi}. Gün!")
        elif kullanici.son_aktif_tarihi == bugun- timedelta(days=1):
            kullanici.gun_serisi += 1
            kullanici.son_aktif_tarihi = bugun
            print(f"Harika! Seriyi bozmadın, serin büyüyor: {kullanici.gun_serisi}. Gün")

        else:
            kullanici.gun_serisi=1
            kullanici.son_aktif_tarihi=bugun
            print("Eyvah! Seriyi bozdun. Olsun, yeniden başlıyoruz. 1. Gün")

        self.repo.session.commit()
        return kullanici.gun_serisi

