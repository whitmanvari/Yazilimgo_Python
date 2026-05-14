#ders yükleme cevap doğrulama işlemleri
from dal.ders_repository import DersRepository

class DersServisi:
    def __init__(self,ders_repo: DersRepository):
        self.repo = ders_repo

    def ders_icerigi_getir(self, ders_id: int):
        return self.repo.id_ile_getir(ders_id)
    
    def modulun_derslerini_getir(self, modul_id: int):
        return self.repo.module_gore_getir(modul_id)
    
    def cevap_dogrula(self, ders_id:int, verilen_cevap: str) -> bool: 
        ders = self.repo.id_ile_getir(ders_id)
        if not ders or not ders.dogru_cevap:
            return False
        beklenen = str(ders.dogru_cevap).strip().lower()
        gelen= str(verilen_cevap).strip().lower()

        return beklenen==gelen