import tkinter as tk
from dal.database import DatabaseManager
from dal.kullanici_repository import KullaniciRepository
from dal.ders_repository import DersRepository
from bll.kullanici_servisi import KullaniciServisi
from bll.ders_servisi import DersServisi
from bll.xp_servisi import XPServisi 
from presentation.screens.ana_menu_ekrani import AnaMenuEkrani
from presentation.screens.ders_ekrani import DersEkrani
from presentation.screens.giris_ekrani import GirisEkrani
from presentation.screens.profil_ekrani import ProfilEkrani
from presentation.screens.kazanimlar_ekrani import KazanimlarEkrani

def main():
    db = DatabaseManager()
    session = db.get_session()
    
    kullanici_repo = KullaniciRepository(session)
    ders_repo = DersRepository(session)
    
    kullanici_servisi = KullaniciServisi(kullanici_repo)
    ders_servisi = DersServisi(ders_repo)
    
    xp_servisi = XPServisi(kullanici_repo) 

    root = tk.Tk()
    root.title("YazılımGo - Öğrenci Eğitim Platformu")
    root.geometry("800x500")

    def sayfaya_git(hedef_ekran_adi, secilen_ders=None):
        giris_ekrani.pack_forget() 
        ana_menu.pack_forget()
        ders_ekrani.pack_forget()
        profil_ekrani.pack_forget()
        kazanimlar_ekrani.pack_forget()

        if hedef_ekran_adi == "GirisEkrani":
            giris_ekrani.pack(fill="both", expand=True)
            
        elif hedef_ekran_adi == "AnaMenu":
            ana_menu.pack(fill="both", expand=True)
            
        elif hedef_ekran_adi == "DersEkrani":
            ders_ekrani.pack(fill="both", expand=True)
            if secilen_ders:
                ders_ekrani.aktif_dersi_ayarla(secilen_ders)
        elif hedef_ekran_adi == "ProfilEkrani":
            profil_ekrani.pack(fill="both", expand=True)
            # Geçiş yaparken veritabanından aktif kullanıcıyı bulup profile yolluyoruz
            kullanici = kullanici_servisi.repo.id_ile_getir(ana_menu.aktif_kullanici_id)
            profil_ekrani.verileri_yukle(kullanici)

        elif hedef_ekran_adi == "KazanimlarEkrani":
            kazanimlar_ekrani.pack(fill="both", expand=True)
            kazanimlar_ekrani.verileri_yukle([]) #en başta rozetler boş
    #bll bağlantısı kurdum
    def kullanici_girisi_kontrol_et(kullanici_adi):
        # Veritabanındaki tüm kullanıcıları çekip isme göre arıyorum
        tum_kullanicilar = kullanici_repo.tum_kullanicilari_getir()
        eslesen_kullanici = None
        
        for k in tum_kullanicilar:
            if k.kullanici_adi.lower() == kullanici_adi.lower():
                eslesen_kullanici = k
                break
                
        if eslesen_kullanici:
            # Kullanıcı bulundu! Ana menüye ID'yi ver ve sayfayı değiştir
            ana_menu.aktif_kullanici_id = eslesen_kullanici.kullanici_id
            ana_menu.verileri_yukle()
            sayfaya_git("AnaMenu")
        else:
            # Kullanıcı yoksa ekrana hata bassın dedim
            giris_ekrani.hata_goster("Kullanıcı bulunamadı!")


    def ders_basarili_oldu(ders):
        aktif_kullanici_id = ana_menu.aktif_kullanici_id
        print(f"{ders.ders_basligi} başarıyla geçildi. Veritabanı güncelleniyor...")
        
        #kullanıcıya xp ekle
        if aktif_kullanici_id:
            xp_servisi.xp_ekle(kullanici_id=aktif_kullanici_id, kazanilan_xp=50)
            ana_menu.verileri_yukle()

    giris_ekrani= GirisEkrani(root, giris_komutu=kullanici_girisi_kontrol_et)

    ana_menu = AnaMenuEkrani(
        root, 
        kullanici_servisi, 
        ders_servisi, 
        sayfa_gecis_komutu=lambda ders: sayfaya_git("DersEkrani", ders),
        profile_git_komutu=lambda: sayfaya_git("ProfilEkrani"),
        kazanimlara_git_komutu=lambda: sayfaya_git("KazanimlarEkrani")
    )
    
    ders_ekrani = DersEkrani(
        root, 
        ana_menuye_don_komutu=lambda: sayfaya_git("AnaMenu"),
        ders_tamamlandi_komutu=ders_basarili_oldu # Callback ataması yaptım
    )

    profil_ekrani = ProfilEkrani(
        root,
        ana_menuye_don_komutu=lambda: sayfaya_git("AnaMenu")
    )
    kazanimlar_ekrani = KazanimlarEkrani(
        root,
        ana_menuye_don_komutu=lambda: sayfaya_git("AnaMenu")

    )

   
    sayfaya_git("GirisEkrani")

    root.mainloop()

if __name__ == "__main__":
    main()