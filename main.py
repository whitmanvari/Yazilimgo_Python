import tkinter as tk
from dal.database import DatabaseManager
from dal.kullanici_repository import KullaniciRepository
from dal.ders_repository import DersRepository
from bll.kullanici_servisi import KullaniciServisi
from bll.ders_servisi import DersServisi
from presentation.screens.ana_menu_ekrani import AnaMenuEkrani
from presentation.screens.ders_ekrani import DersEkrani

def main():
    db = DatabaseManager()
    session = db.get_session()
    
    kullanici_repo = KullaniciRepository(session)
    ders_repo = DersRepository(session)
    
    kullanici_servisi = KullaniciServisi(kullanici_repo)
    ders_servisi = DersServisi(ders_repo)

    root = tk.Tk()
    root.title("YazılımGo - Öğrenci Eğitim Platformu")
    root.geometry("800x500")

    def sayfaya_git(hedef_ekran_adi, secilen_ders=None):
        ana_menu.pack_forget()
        ders_ekrani.pack_forget()

        if hedef_ekran_adi == "AnaMenu":
            ana_menu.pack(fill="both", expand=True)
            
        elif hedef_ekran_adi == "DersEkrani":
            ders_ekrani.pack(fill="both", expand=True)
            if secilen_ders:
                ders_ekrani.aktif_dersi_ayarla(secilen_ders)

    # ekranları oluşturacağım
    ana_menu = AnaMenuEkrani(
        root, 
        kullanici_servisi, 
        ders_servisi, 
        sayfa_gecis_komutu=lambda ders: sayfaya_git("DersEkrani", ders)
    )
    
    # Ders ekranına da ana menüye dönmesi için komut gönderdim
    ders_ekrani = DersEkrani(root, ana_menuye_don_komutu=lambda: sayfaya_git("AnaMenu"))

    ana_menu.verileri_yukle()
    sayfaya_git("AnaMenu")

    root.mainloop()

if __name__ == "__main__":
    main()