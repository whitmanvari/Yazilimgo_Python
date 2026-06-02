from datetime import datetime
from entities.kullaniciKazanim import KullaniciKazanim 

class KazanimServisi:
    def __init__(self, kazanim_repo, kullanici_repo):
        self.kazanim_repo = kazanim_repo
        self.kullanici_repo = kullanici_repo

    def rozetleri_kontrol_et_ve_ver(self, kullanici_id):
        """Kullanıcının istatistiklerine bakar, hak ettiği yeni rozetleri veritabanına kaydeder."""
        kullanici = self.kullanici_repo.id_ile_getir(kullanici_id)
        if not kullanici:
            return []

        # Sistemdeki tüm rozet kurallarını getir
        tum_rozetler = self.kazanim_repo.tum_kazanim_tanimlarini_getir() 
        
        # Kullanıcının zaten aldığı rozetleri getir (Tekrar aynı rozeti vermemek için)
        sahip_olunanlar = self.kazanim_repo.kullanicinin_kazanimlarini_getir(kullanici_id)
        sahip_olunan_id_listesi = [k.kazanim_id for k in sahip_olunanlar]

        yeni_kazanilanlar = []

        # Rozetleri tek tek kontrol et
        for rozet in tum_rozetler:
            if rozet.kazanim_id in sahip_olunan_id_listesi:
                continue 

            kazandi_mi = False

          
            if rozet.kosul_turu == "ilk_ders":
                if kullanici.toplam_xp > 0: 
                    kazandi_mi = True
            
            elif rozet.kosul_turu == "xp_esigi":
                if kullanici.toplam_xp >= rozet.kosul_degeri:
                    kazandi_mi = True
            elif rozet.kosul_turu == "ders_sayisi":
                if len(kullanici.ilerlemeler) >= rozet.kosul_degeri:
                    kazandi_mi = True
            
           
            if kazandi_mi:
                yeni_kazanim = KullaniciKazanim(
                    kullanici_id=kullanici.kullanici_id,
                    kazanim_id=rozet.kazanim_id,
                    kazanilma_tarih=datetime.now()
                )
                self.kazanim_repo.kullaniciya_kazanim_ekle(yeni_kazanim.kullanici_id,yeni_kazanim.kazanim_id)
                yeni_kazanilanlar.append(rozet)

        return yeni_kazanilanlar