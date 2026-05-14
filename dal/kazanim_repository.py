#kazanım crud işlemleri

from sqlalchemy.orm import Session

from entities.kazanim import KazanimTanimi
from entities.kullaniciKazanim import KullaniciKazanim


class KazanimRepository:
    def __init__(self, session: Session):
        self.session=session
    
    def tum_kazanim_tanimlarini_getir(self):
        return self.session.query(KazanimTanimi).all() #entities kazanımdan geliyor
    
    def kullanicinin_kazanimlarini_getir(self, kullanici_id: int):
        return self.session.query(KullaniciKazanim).filter(KullaniciKazanim.kullanici_id==kullanici_id).all()
    
    def kullaniciya_kazanim_ekle(self, kullanici_id: int, kazanim_id: int):
        yeni_kazanim= KullaniciKazanim(kullanici_id=kullanici_id, kazanim_id=kazanim_id)
        self.session.add(yeni_kazanim)
        self.session.commit()
        return yeni_kazanim
    
    