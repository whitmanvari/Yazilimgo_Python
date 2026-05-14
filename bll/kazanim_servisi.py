#rozet tetikleme motoru
from dal.kazanim_repository import KazanimRepository

class KazanimServisi:
    def __init__(self, kazanim_repo: KazanimRepository):
        self.repo=kazanim_repo

    def rozet_ver(self, kullanici_id: int, kazanim_id:int):
        #rozet zaten varsa tekrar verme
        kullanici_rozetleri= self.repo.kullanicinin_kazanimlarini_getir(kullanici_id)

        for rozet in kullanici_rozetleri:
            if rozet.kazanim_id == kazanim_id:
                print("Kullanıcı bu rozete zaten sahip! Tekrar verilemedi..")
                return False
            
        self.repo.kullaniciya_kazanim_ekle(kullanici_id, kazanim_id)
        print("Mükemmel, yeni bir rozet kazandınız!")
        return True
            