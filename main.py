import tkinter as tk
from dal.database import DatabaseManager
from dal.kullanici_repository import KullaniciRepository
from dal.ders_repository import DersRepository
from dal.kazanim_repository import KazanimRepository
from bll.kullanici_servisi import KullaniciServisi
from bll.ders_servisi import DersServisi
from bll.xp_servisi import XPServisi 
from bll.kazanim_servisi import KazanimServisi
from bll.analytics_engine import AnalyticsEngine
from entities.ilerleme import IlerlemeKaydi
from datetime import datetime

from presentation.screens.ana_menu_ekrani import AnaMenuEkrani
from presentation.screens.ders_ekrani import DersEkrani
from presentation.screens.giris_ekrani import GirisEkrani
from presentation.screens.profil_ekrani import ProfilEkrani
from presentation.screens.kazanimlar_ekrani import KazanimlarEkrani
from presentation.components.sidebar import SidebarWidget 

def main():
    db = DatabaseManager()
    session = db.get_session()
    
    kullanici_repo = KullaniciRepository(session)
    ders_repo = DersRepository(session)
    kazanim_repo = KazanimRepository(session)
    
    kullanici_servisi = KullaniciServisi(kullanici_repo)
    ders_servisi = DersServisi(ders_repo)
    kazanim_servisi = KazanimServisi(kazanim_repo, kullanici_repo)
    xp_servisi = XPServisi(kullanici_repo) 
    analytics_engine = AnalyticsEngine(kullanici_repo)

    root = tk.Tk()
    root.title("YazılımGo - Öğrenci Eğitim Platformu")
    root.geometry("1100x900")

    sidebar = SidebarWidget(root, 
                            sayfa_gecis_komutu=lambda hedef: sayfaya_git(hedef), 
                            cikis_komutu=lambda: sayfaya_git("GirisEkrani"))
    sidebar.pack(side="left", fill="y")
    
    main_content = tk.Frame(root, bg="#ffffff")
    main_content.place(x=50, y=0, relwidth=1, relheight=1, width=-50)

    sidebar = SidebarWidget(root, 
                            sayfa_gecis_komutu=lambda hedef: sayfaya_git(hedef), 
                            cikis_komutu=lambda: sayfaya_git("GirisEkrani"))
    sidebar.place(x=0, y=0, relheight=1, width=50)

    def sayfaya_git(hedef, veri=None):
        for widget in main_content.winfo_children():
            widget.pack_forget()

        if hedef == "GirisEkrani":
            sidebar.place_forget() 
            ana_menu.aktif_kullanici_id = None
            main_content.place(x=0, y=0, relwidth=1, relheight=1, width=0)
        else:
            sidebar.place(x=0, y=0, relheight=1, width=sidebar.winfo_width() if sidebar.winfo_width() >10 else 50)
            main_content.place(x=50, y=0, relwidth=1,width=-50)

        if hedef == "GirisEkrani":
            giris_ekrani.pack(in_=main_content, fill="both", expand=True)
            
        elif hedef == "AnaMenu":
            ana_menu.pack(in_=main_content, fill="both", expand=True)
            
        elif hedef == "DersEkrani":
            ders_ekrani.pack(in_=main_content, fill="both", expand=True)
            if veri: ders_ekrani.aktif_dersi_ayarla(veri)
            
        elif hedef == "ProfilEkrani":
            profil_ekrani.pack(in_=main_content, fill="both", expand=True)
            kullanici = kullanici_servisi.repo.id_ile_getir(ana_menu.aktif_kullanici_id)
            analytics_engine.xp_liderlik_grafigi_ciz()
            profil_ekrani.verileri_yukle(kullanici)
            
        elif hedef == "KazanimlarEkrani":
            kazanimlar_ekrani.pack(in_=main_content, fill="both", expand=True)
            kullanici = kullanici_servisi.repo.id_ile_getir(ana_menu.aktif_kullanici_id)
            kazanilan_rozetler = [k.kazanim_tanimi for k in kullanici.kazanimlar] if kullanici else []
            kazanimlar_ekrani.verileri_yukle(kazanilan_rozetler)

    def kullanici_girisi_kontrol_et(kullanici_adi, sifre):
        kullanici = next((k for k in kullanici_repo.tum_kullanicilari_getir() 
                         if k.kullanici_adi.lower() == kullanici_adi.lower()), None)
        if kullanici and kullanici_servisi.giris_yap(kullanici.kullanici_id, sifre):
            ana_menu.aktif_kullanici_id = kullanici.kullanici_id
            ana_menu.verileri_yukle()
            sayfaya_git("AnaMenu")
        else:
            giris_ekrani.hata_goster("Hatalı giriş bilgileri!")

    def kullanici_kaydi_yap(kullanici_adi, email, sifre):
        if kullanici_servisi.kayit_ol(kullanici_adi, email, sifre):
            giris_ekrani.hata_goster("Kayıt başarılı!", basarili_mi=True)
            giris_ekrani.mod_degistir()
        else:
            giris_ekrani.hata_goster("Kayıt başarısız!")

    def ders_basarili_oldu(ders):
        uid = ana_menu.aktif_kullanici_id 
        kullanici = kullanici_servisi.repo.id_ile_getir(uid)
        if kullanici and not any(i.ders_id == ders.ders_id and i.durum == 'tamamlandi' for i in kullanici.ilerlemeler):
            xp_servisi.xp_ekle(uid, ders.kazanilan_xp)
            kullanici_repo.session.add(IlerlemeKaydi(kullanici_id=uid, ders_id=ders.ders_id, durum="tamamlandi", tamamlanma_tarihi=datetime.now(), kazanilan_xp=ders.kazanilan_xp))
            kullanici_repo.session.commit()
            kazanim_servisi.rozetleri_kontrol_et_ve_ver(uid)
            ana_menu.verileri_yukle()

    giris_ekrani = GirisEkrani(main_content, kullanici_girisi_kontrol_et, kullanici_kaydi_yap)
    ana_menu = AnaMenuEkrani(main_content, kullanici_servisi, ders_servisi, 
                             lambda d: sayfaya_git("DersEkrani", d),
                             lambda: sayfaya_git("ProfilEkrani"),
                             lambda: sayfaya_git("KazanimlarEkrani"))
                             
    ders_ekrani = DersEkrani(main_content, lambda: sayfaya_git("AnaMenu"), ders_basarili_oldu)
    profil_ekrani = ProfilEkrani(main_content, lambda: sayfaya_git("AnaMenu"), kullanici_repo)
    kazanimlar_ekrani = KazanimlarEkrani(main_content, lambda: sayfaya_git("AnaMenu"))

    sayfaya_git("GirisEkrani")
    root.mainloop()

if __name__ == "__main__":
    main()