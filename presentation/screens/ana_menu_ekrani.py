from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea
from PyQt6.QtCore import Qt

from presentation.components.xp_bar import XPBar
from presentation.components.rozet_widget import RozetWidget
from presentation.components.ders_karti import DersKarti

class AnaMenuEkrani(QWidget):
    def __init__(self, parent=None, kullanici_servisi=None, ders_servisi=None, 
                 sayfa_gecis_komutu=None, profile_git_komutu=None, kazanimlara_git_komutu=None):
        super().__init__(parent)

        self.kullanici_servisi = kullanici_servisi
        self.ders_servisi = ders_servisi
        self.sayfa_gecis_komutu = sayfa_gecis_komutu
        self.profile_git_komutu = profile_git_komutu
        self.kazanimlara_git_komutu = kazanimlara_git_komutu
        self.aktif_kullanici_id = None

        self.init_ui()

    def init_ui(self):
        self.ana_layout = QVBoxLayout(self)
        self.ana_layout.setContentsMargins(0, 0, 0, 0)
        self.ana_layout.setSpacing(0)

        self.ust_panel = QWidget()
        self.ust_panel.setStyleSheet("background-color: #000000;")
        self.ust_panel.setFixedHeight(70)
        ust_layout = QHBoxLayout(self.ust_panel)
        ust_layout.setContentsMargins(20, 0, 20, 0)

        self.lbl_hosgeldin = QLabel("Hoş Geldin!")
        self.lbl_hosgeldin.setStyleSheet("font-family: cursive; font-size: 24px; font-weight: bold; color: #ffffff;")
        ust_layout.addWidget(self.lbl_hosgeldin)

        ust_layout.addStretch()

        self.btn_profil = QPushButton("Profilim")
        self.btn_profil.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_profil.setStyleSheet("""
            QPushButton {
                background-color: #790909;
                color: white; font-weight: bold; font-size: 14px;
                padding: 10px 20px; border-radius: 6px;
            }
            QPushButton:hover { background-color: #570B0B; }
        """)
        self.btn_profil.clicked.connect(self.profile_git_komutu)
        ust_layout.addWidget(self.btn_profil)

        self.ana_layout.addWidget(self.ust_panel)

        self.govde_widget = QWidget()
        govde_layout = QHBoxLayout(self.govde_widget)
        govde_layout.setContentsMargins(0, 0, 0, 0)
        govde_layout.setSpacing(0)

        self.sol_panel = QWidget()
        self.sol_panel.setFixedWidth(280)
        self.sol_panel.setStyleSheet("background-color: #2b2b2b;")
        sol_layout = QVBoxLayout(self.sol_panel)
        sol_layout.setContentsMargins(20, 30, 20, 30)
        sol_layout.setSpacing(25)

        self.xp_bar = XPBar()
        sol_layout.addWidget(self.xp_bar)

        self.rozet_widget = RozetWidget()
        sol_layout.addWidget(self.rozet_widget)

        self.btn_tum_rozetler = QPushButton("Tümünü Gör ➔")
        self.btn_tum_rozetler.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_tum_rozetler.setStyleSheet("QPushButton { color: white; border: none; font-weight: bold; font-size: 13px; text-align: right; } QPushButton:hover { color: #FAA2A2; }")
        self.btn_tum_rozetler.clicked.connect(self.kazanimlara_git_komutu)
        sol_layout.addWidget(self.btn_tum_rozetler)
        sol_layout.addStretch()

        govde_layout.addWidget(self.sol_panel)

        self.sag_panel = QWidget()
        self.sag_panel.setStyleSheet("background-color: #ffffff;")
        sag_layout = QVBoxLayout(self.sag_panel)
        sag_layout.setContentsMargins(30, 30, 30, 30)

        self.lbl_dersler = QLabel("Mevcut Dersler")
        self.lbl_dersler.setStyleSheet("font-size: 22px; font-weight: bold; color: #333;")
        sag_layout.addWidget(self.lbl_dersler)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; background-color: white; }")

        self.ders_listesi_widget = QWidget()
        self.ders_listesi_widget.setStyleSheet("background-color: white;")
        self.ders_listesi_layout = QVBoxLayout(self.ders_listesi_widget)
        self.ders_listesi_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.ders_listesi_layout.setSpacing(15)

        self.scroll_area.setWidget(self.ders_listesi_widget)
        sag_layout.addWidget(self.scroll_area)

        govde_layout.addWidget(self.sag_panel)
        self.ana_layout.addWidget(self.govde_widget)

    def verileri_yukle(self):
        kullanici = self.kullanici_servisi.repo.id_ile_getir(self.aktif_kullanici_id)
        if kullanici:
            self.xp_bar.guncelle(kullanici.toplam_xp, kullanici.seviye)
            rozetler = [k.kazanim_tanimi.kazanim_adi for k in kullanici.kazanimlar]

            for i in reversed(range(self.ders_listesi_layout.count())): 
                widget = self.ders_listesi_layout.itemAt(i).widget()
                self.ders_listesi_layout.removeWidget(widget)
                widget.setParent(None)

            self.rozet_widget.rozetleri_goster(rozetler)
            
        dersler = self.ders_servisi.modulun_derslerini_getir(modul_id=1)
        if dersler:
            tamamlanan_idler = [i.ders_id for i in kullanici.ilerlemeler if i.durum == 'tamamlandi']

            for ders in dersler:
                durum_tamamlandi = ders.ders_id in tamamlanan_idler
                kart = DersKarti(
                    baslik=ders.ders_basligi,
                    tur=ders.ders_turu,
                    komut=lambda checked, d=ders: self.dersi_baslat(d), 
                    tamamlandi_mi=durum_tamamlandi
                )
                self.ders_listesi_layout.addWidget(kart)

    def dersi_baslat(self, ders):
        print(f"{ders.ders_basligi} ekranına geçiliyor...")
        if self.sayfa_gecis_komutu:
            self.sayfa_gecis_komutu(ders)