import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QHBoxLayout
from PyQt6.QtCore import Qt

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

from presentation.components.sidebar import SidebarWidget
from presentation.screens.giris_ekrani import GirisEkrani
from presentation.screens.ana_menu_ekrani import AnaMenuEkrani
from presentation.screens.ders_ekrani import DersEkrani
from presentation.screens.profil_ekrani import ProfilEkrani
from presentation.screens.kazanimlar_ekrani import KazanimlarEkrani

class AnaPencere(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YazılımGo - Öğrenci Eğitim Platformu")
        self.resize(1100, 900)
        
        db = DatabaseManager()
        session = db.get_session()
        
        self.kullanici_repo = KullaniciRepository(session)
        ders_repo = DersRepository(session)
        kazanim_repo = KazanimRepository(session)
        
        self.kullanici_servisi = KullaniciServisi(self.kullanici_repo)
        self.ders_servisi = DersServisi(ders_repo)
        self.kazanim_servisi = KazanimServisi(kazanim_repo, self.kullanici_repo)
        self.xp_servisi = XPServisi(self.kullanici_repo) 
        self.analytics_engine = AnalyticsEngine(self.kullanici_repo)

        self.aktif_kullanici_id = None

        merkez_widget = QWidget()
        self.setCentralWidget(merkez_widget)
        
        self.ana_layout = QHBoxLayout(merkez_widget)
        self.ana_layout.setContentsMargins(0, 0, 0, 0) 
        self.ana_layout.setSpacing(0)

        # 1. Sidebar Bileşeni
        self.sidebar = SidebarWidget(
            sayfa_gecis_komutu=self.sayfaya_git,
            cikis_komutu=lambda: self.sayfaya_git("GirisEkrani")
        )
        self.ana_layout.addWidget(self.sidebar)
        self.sidebar.hide() # Giriş ekranında gizli başlar

        self.ekranlar = QStackedWidget()
        self.ana_layout.addWidget(self.ekranlar)

        
        # Index 0: Giriş Ekranı
        self.giris_ekrani = GirisEkrani(
            giris_komutu=self.kullanici_girisi_kontrol_et, 
            kayit_komutu=self.kullanici_kaydi_yap
        )
        self.ekranlar.addWidget(self.giris_ekrani) 

        # Index 1: Ana Menü Ekranı 
        self.ana_menu_ekrani = AnaMenuEkrani(
            kullanici_servisi=self.kullanici_servisi,
            ders_servisi=self.ders_servisi,
            sayfa_gecis_komutu=lambda d: self.sayfaya_git("DersEkrani", d),
            profile_git_komutu=lambda: self.sayfaya_git("ProfilEkrani"),
            kazanimlara_git_komutu=lambda: self.sayfaya_git("KazanimlarEkrani")
        )
        self.ekranlar.addWidget(self.ana_menu_ekrani)

        # Index 2: Ders Ekranı
        self.ders_ekrani = DersEkrani(
            ana_menuye_don_komutu=lambda: self.sayfaya_git("AnaMenu"),
            ders_tamamlandi_komutu=self.ders_basarili_oldu
        )
        self.ekranlar.addWidget(self.ders_ekrani)

        # Index 3: Profil Ekranı
        self.profil_ekrani = ProfilEkrani(
            ana_menuye_don_komutu=lambda: self.sayfaya_git("AnaMenu"),
            kullanici_repo=self.kullanici_repo
        )
        self.ekranlar.addWidget(self.profil_ekrani)

        # Index 4: Kazanımlar Ekranı
        self.kazanimlar_ekrani = KazanimlarEkrani(
            ana_menuye_don_komutu=lambda: self.sayfaya_git("AnaMenu")
        )
        self.ekranlar.addWidget(self.kazanimlar_ekrani)

        self.sayfaya_git("GirisEkrani")

    def sayfaya_git(self, hedef, veri=None):
        if hedef == "GirisEkrani":
            self.sidebar.hide()
            self.aktif_kullanici_id = None
            self.ekranlar.setCurrentIndex(0) 
            
        elif hedef == "AnaMenu":
            self.sidebar.show()
            self.ana_menu_ekrani.aktif_kullanici_id = self.aktif_kullanici_id
            self.ana_menu_ekrani.verileri_yukle()
            self.ekranlar.setCurrentIndex(1) 
            
        elif hedef == "DersEkrani":
            self.sidebar.hide() 
            if veri: 
                self.ders_ekrani.aktif_dersi_ayarla(veri)
            self.ekranlar.setCurrentIndex(2)
            
        elif hedef == "ProfilEkrani":
            self.sidebar.show()
            kullanici = self.kullanici_repo.id_ile_getir(self.aktif_kullanici_id)
            self.profil_ekrani.verileri_yukle(kullanici)
            self.ekranlar.setCurrentIndex(3)
            
        elif hedef == "KazanimlarEkrani":
            self.sidebar.show()
            kullanici = self.kullanici_repo.id_ile_getir(self.aktif_kullanici_id)
            kazanimlar = kullanici.kazanimlar if kullanici else []
            self.kazanimlar_ekrani.verileri_yukle(kazanimlar)
            self.ekranlar.setCurrentIndex(4)

    def kullanici_girisi_kontrol_et(self, kullanici_adi, sifre):
        kullanici = next((k for k in self.kullanici_repo.tum_kullanicilari_getir() 
                         if k.kullanici_adi.lower() == kullanici_adi.lower()), None)
                         
        if kullanici and self.kullanici_servisi.giris_yap(kullanici.kullanici_id, sifre):
            self.aktif_kullanici_id = kullanici.kullanici_id
            self.sayfaya_git("AnaMenu")
        else:
            self.giris_ekrani.hata_goster("Hatalı giriş bilgileri!")

    def kullanici_kaydi_yap(self, kullanici_adi, email, sifre):
        if self.kullanici_servisi.kayit_ol(kullanici_adi, email, sifre):
            self.giris_ekrani.hata_goster("Kayıt başarılı!", basarili_mi=True)
            self.giris_ekrani.mod_degistir()
        else:
            self.giris_ekrani.hata_goster("Kayıt başarısız!")

    def ders_basarili_oldu(self, ders):
        uid = self.aktif_kullanici_id 
        kullanici = self.kullanici_repo.id_ile_getir(uid)
        
        if kullanici and not any(i.ders_id == ders.ders_id and i.durum == 'tamamlandi' for i in kullanici.ilerlemeler):
            # XP Ekle
            self.xp_servisi.xp_ekle(uid, ders.kazanilan_xp)
            
            # İlerlemeyi Veritabanına Kaydet
            yeni_ilerleme = IlerlemeKaydi(kullanici_id=uid, ders_id=ders.ders_id, 
                                          durum="tamamlandi", tamamlanma_tarihi=datetime.now(), 
                                          kazanilan_xp=ders.kazanilan_xp)
            self.kullanici_repo.session.add(yeni_ilerleme)
            self.kullanici_repo.session.commit()
            
            # Rozet Kontrolü Yap
            self.kazanim_servisi.rozetleri_kontrol_et_ve_ver(uid)
            
            self.ana_menu_ekrani.verileri_yukle()

def main():
    app = QApplication(sys.argv)
    pencere = AnaPencere()
    pencere.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()