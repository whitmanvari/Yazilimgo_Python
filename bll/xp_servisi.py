from dal.kullanici_repository import KullaniciRepository

class XPServisi:
    def __init__(self, kullanici_repo: KullaniciRepository):
        self.kullanici_repo = kullanici_repo
        #iş kuralı: kullanıcı her 100xp topladığında 1 seviye atlasın
        self.SEVIYE_SINIRI = 100

    def xp_ekle(self, kullanici_id: int, kazanilan_xp: int):
        #kullanıcıya xp eklesin diye yazdığım methot, bir noktadan sonra seviye de atlatacak (100xpde bir)
        kullanici= self.kullaniic_repo.id_ile_getir(kullanici_id)
        if not kullanici:
            print("Hata: Kullanıcı bulunamadı!")
            return None
        #xp'sini mevcut xp'sinin üzerine ekleyeceğim
        kullanici.toplam_xp += kazanilan_xp
        print(f"Tebrikler! {kazanilan_xp} kadar XP kazandın!")
        #seviye atlaması için de örneğin 150 // 100 = 1 ve +1, yani bu demek ki üzerine 1 seviye ekle
        yeni_seviye= (kullanici.toplam_xp // self.SEVIYE_SINIRI) + 1
        if yeni_seviye >kullanici.seviye:
            print(f"Seviye atladın! Yeni seviyen: {kullanici.seviye}")

        self.kullanici_repo.session.commit()
        return kullanici