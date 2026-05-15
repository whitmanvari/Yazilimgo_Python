import tkinter as tk
from dal.database import DatabaseManager
from dal.kullanici_repository import KullaniciRepository
from dal.ders_repository import DersRepository
from bll.kullanici_servisi import KullaniciServisi
from bll.ders_servisi import DersServisi
from presentation.screens.ana_menu_ekrani import AnaMenuEkrani

def main():
    db = DatabaseManager()
    session = db.get_session()
    
    kullanici_repo = KullaniciRepository(session)
    ders_repo = DersRepository(session)
    
    kullanici_servisi = KullaniciServisi(kullanici_repo)
    ders_servisi = DersServisi(ders_repo)

    root = tk.Tk()
    root.title("YazılımGo - Öğrenci Paneli")
    root.geometry("800x500")

    ana_menu = AnaMenuEkrani(root, kullanici_servisi, ders_servisi)
    ana_menu.pack(fill="both", expand=True)
    
    ana_menu.verileri_yukle()

    root.mainloop()

if __name__ == "__main__":
    main()