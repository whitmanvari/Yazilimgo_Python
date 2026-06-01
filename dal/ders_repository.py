from sqlalchemy.orm import Session
from entities.ders import Ders
 #dependency injection yaptım. 
class DersRepository:
    def __init__(self, session: Session):
        self.session=session

    def id_ile_getir(self, ders_id: int):
        return self.session.query(Ders).filter(Ders.ders_id==ders_id).first()
    
    def module_gore_getir(self,modul_id: int):
        return self.session.query(Ders).filter(Ders.modul_id==modul_id).order_by(Ders.sira_no).all()
    
