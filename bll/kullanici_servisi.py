import hashlib
from dal.kullanici_repository import KullaniciRepository

class KullaniciServisi:
    def __init__(self, repository: KullaniciRepository):
        self.repo=repository

    def _sifre_hashle(self, sifre: str) -> str:
        return hashlib.sha256(sifre.encode()).hexdigest()
    
    def kayit_ol(self, kullanici_adi: str, email: str, sifre: str):
        if len(sifre) <6:
            print("Hata! Şifre en az 6 karakterli olmalıdır!")
            return None
        hashli_sifre = self._sifre_hashle(sifre)
        return self.repo.kullanici_ekle(kullanici_adi, email, hashli_sifre)
    
    def giris_yap(self, kullanici_id: int, girilen_sifre: str):
        kullanici = self.repo.id_ile_getir(kullanici_id)
        if not kullanici: return False
        return kullanici.parola_hash == self._sifre_hashle(girilen_sifre)