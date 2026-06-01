from sqlalchemy.orm import Session
from entities.ilerleme import IlerlemeKaydi

class IlerlemeRepository:
    def __init__(self, session: Session):
        self.session = session

    # Belirli bir kullanıcının, belirli bir dersteki ilerlemesini getir
    def kullanici_ders_ilerleme_getir(self, kullanici_id: int, ders_id: int):
        return self.session.query(IlerlemeKaydi).filter(
            IlerlemeKaydi.kullanici_id == kullanici_id,
            IlerlemeKaydi.ders_id == ders_id
        ).first()

    # Kullanıcının tüm ders geçmişini getir
    def kullanicinin_tum_ilerlemelerini_getir(self, kullanici_id: int):
        return self.session.query(IlerlemeKaydi).filter(IlerlemeKaydi.kullanici_id == kullanici_id).all()

    # Yeni bir ilerleme kaydı ekle
    def ilerleme_ekle(self, ilerleme_kaydi: IlerlemeKaydi):
        self.session.add(ilerleme_kaydi)
        self.session.commit()