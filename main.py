import tkinter as tk
from dal.database import DatabaseManager
from dal.kullanici_repository import KullaniciRepository
from dal.ders_repository import DersRepository
from dal.kazanim_repository import KazanimRepository
from bll.kullanici_servisi import KullaniciServisi
from bll.ders_servisi import DersServisi
from bll.xp_servisi import XPServisi 
from bll.kazanim_servisi import KazanimServisi
from presentation.screens.ana_menu_ekrani import AnaMenuEkrani
from presentation.screens.ders_ekrani import DersEkrani
from presentation.screens.giris_ekrani import GirisEkrani
from presentation.screens.profil_ekrani import ProfilEkrani
from presentation.screens.kazanimlar_ekrani import KazanimlarEkrani
from bll.analytics_engine import AnalyticsEngine

def main():
    db = DatabaseManager()
    session = db.get_session()
    
    kullanici_repo = KullaniciRepository(session)
    ders_repo = DersRepository(session)
    kazanim_repo=KazanimRepository(session)
    
    kullanici_servisi = KullaniciServisi(kullanici_repo)
    ders_servisi = DersServisi(ders_repo)
    
    kazanim_servisi=KazanimServisi(kazanim_repo, kullanici_repo)
    
    xp_servisi = XPServisi(kullanici_repo) 

    root = tk.Tk()
    root.title("YazılımGo - Öğrenci Eğitim Platformu")
    root.geometry("900x600")
    root.minsize(800,500)

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
        elif hedef_ekran_adi == "ProfilEkrani":
            profil_ekrani.pack(fill="both", expand=True)
            kullanici = kullanici_servisi.repo.id_ile_getir(ana_menu.aktif_kullanici_id)
            
            # Öğrenci profile girer girmez güncel tabloyu anlık olarak çizdirip kaydediyoruz
            analytics_engine.xp_liderlik_grafigi_ciz()
            profil_ekrani.verileri_yukle(kullanici)

        elif hedef_ekran_adi == "KazanimlarEkrani":
            kazanimlar_ekrani.pack(fill="both", expand=True)
            kullanici = kullanici_servisi.repo.id_ile_getir(ana_menu.aktif_kullanici_id)
            
            kazanilan_rozetler = []
            if kullanici and kullanici.kazanimlar:
                for k in kullanici.kazanimlar:
                    kazanilan_rozetler.append(k.kazanim_tanimi)
            kazanimlar_ekrani.verileri_yukle(kazanilan_rozetler) #en başta rozetler boş
    #bll bağlantısı kurdum
    def kullanici_girisi_kontrol_et(kullanici_adi, sifre):
        tum_kullanicilar = kullanici_repo.tum_kullanicilari_getir()
        eslesen_kullanici = next((k for k in tum_kullanicilar if k.kullanici_adi.lower() == kullanici_adi.lower()), None)
                
        if eslesen_kullanici:
            if kullanici_servisi.giris_yap(eslesen_kullanici.kullanici_id, sifre):
                ana_menu.aktif_kullanici_id = eslesen_kullanici.kullanici_id
                ana_menu.verileri_yukle()
                sayfaya_git("AnaMenu")
            else:
                giris_ekrani.hata_goster("Hatalı şifre girdiniz!")
        else:
            giris_ekrani.hata_goster("Kullanıcı bulunamadı!")

    def kullanici_kaydi_yap(kullanici_adi, email, sifre):
        yeni_kullanici = kullanici_servisi.kayit_ol(kullanici_adi, email, sifre)
        if yeni_kullanici:
            giris_ekrani.hata_goster("Kayıt başarılı! Şimdi giriş yapabilirsin.", basarili_mi=True)
            giris_ekrani.mod_degistir()
        else:
            giris_ekrani.hata_goster("Bu isim veya e-posta zaten kullanımda (veya şifre kısa)!")

    def ders_basarili_oldu(ders):
        aktif_kullanici_id = ana_menu.aktif_kullanici_id 
        kullanici = kullanici_servisi.repo.id_ile_getir(aktif_kullanici_id)
        
        if kullanici:
            # Acaba bu dersi daha önce geçmiş miydi?
            zaten_tamamlandi = any(i.ders_id == ders.ders_id and i.durum == 'tamamlandi' for i in kullanici.ilerlemeler)

            if not zaten_tamamlandi:
                print(f"{ders.ders_basligi} İLK KEZ geçildi. {ders.kazanilan_xp} XP ekleniyor...")
                
                # XP'yi versin önce
                xp_servisi.xp_ekle(kullanici_id=aktif_kullanici_id, kazanilan_xp=ders.kazanilan_xp)
                
                # İlerleme Kaydını veritabanına eklesin
                from entities.ilerleme import IlerlemeKaydi
                from datetime import datetime
                yeni_ilerleme = IlerlemeKaydi(
                    kullanici_id=aktif_kullanici_id,
                    ders_id=ders.ders_id,
                    durum="tamamlandi",
                    tamamlanma_tarihi=datetime.now(),
                    kazanilan_xp=ders.kazanilan_xp
                )
                kullanici_repo.session.add(yeni_ilerleme)
                kullanici_repo.session.commit()

                # Rozet kontrolü yapsın
                yeni_rozetler = kazanim_servisi.rozetleri_kontrol_et_ve_ver(aktif_kullanici_id)
                if yeni_rozetler:
                    for r in yeni_rozetler:
                        print(f"🎉 YENİ ROZET KAZANILDI: {r.kazanim_adi} 🎉")
            else:
                print("Bu ders zaten daha önce tamamlanmış. Tekrar çözüldü, ekstra XP verilmedi.")
            
            ana_menu.verileri_yukle()

    analytics_engine = AnalyticsEngine(kullanici_repo)

    giris_ekrani = GirisEkrani(root, giris_komutu=kullanici_girisi_kontrol_et, kayit_komutu=kullanici_kaydi_yap)
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
        ana_menuye_don_komutu=lambda: sayfaya_git("AnaMenu"),
        kullanici_repo=kullanici_repo

    )
    kazanimlar_ekrani = KazanimlarEkrani(
        root,
        ana_menuye_don_komutu=lambda: sayfaya_git("AnaMenu")

    )

   
    sayfaya_git("GirisEkrani")

    root.mainloop()

if __name__ == "__main__":
    main()