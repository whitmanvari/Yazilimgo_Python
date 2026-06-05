from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from bll.analytics_engine import AnalyticsEngine

class ProfilEkrani(QWidget):
    def __init__(self, parent=None, ana_menuye_don_komutu=None, kullanici_repo=None):
        super().__init__(parent)
        self.ana_menuye_don_komutu = ana_menuye_don_komutu
        self.repo = kullanici_repo
        
        self.init_ui()

    def init_ui(self):
        # Ana Arka Plan
        self.setStyleSheet("QWidget { background-color: #2b2b2b; }")
        
        ana_layout = QVBoxLayout(self)
        ana_layout.setContentsMargins(0, 0, 0, 0)
        ana_layout.setSpacing(0)

        self.header_frame = QWidget()
        self.header_frame.setStyleSheet("background-color: #1e1e1e;")
        self.header_frame.setFixedHeight(60)
        
        header_layout = QHBoxLayout(self.header_frame)
        header_layout.setContentsMargins(15, 0, 20, 0)

        self.btn_geri = QPushButton("⬅ Ana Menüye Dön")
        self.btn_geri.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_geri.setStyleSheet("""
            QPushButton {
                background-color: #FAA2A2;
                color: white;
                font-family: 'DejaVu Sans';
                font-weight: bold;
                font-size: 14px;
                border: none;
                padding: 8px 15px;
                border-radius: 5px;
            }
            QPushButton:hover { background-color: #790909; }
        """)
        if self.ana_menuye_don_komutu:
            self.btn_geri.clicked.connect(self.ana_menuye_don_komutu)
        header_layout.addWidget(self.btn_geri)

        self.lbl_baslik = QLabel("Öğrenci Profili")
        self.lbl_baslik.setStyleSheet("font-family: cursive; font-size: 20px; font-weight: bold; color: white;")
        header_layout.addWidget(self.lbl_baslik)
        
        header_layout.addStretch()
        ana_layout.addWidget(self.header_frame)

        icerik_widget = QWidget()
        icerik_layout = QVBoxLayout(icerik_widget)
        icerik_layout.setContentsMargins(20, 20, 20, 20)
        icerik_layout.setSpacing(20)

        self.info_frame = QWidget()
        self.info_frame.setStyleSheet("background-color: #1e1e1e; border-radius: 10px;")
        info_layout = QHBoxLayout(self.info_frame)
        info_layout.setContentsMargins(20, 15, 20, 15)

        self.lbl_isim = QLabel("Öğrenci: ...")
        self.lbl_isim.setStyleSheet("font-size: 18px; font-weight: bold; color: #FAA2A2;")
        info_layout.addWidget(self.lbl_isim)

        self.lbl_seviye = QLabel("🏆 Seviye: 1")
        self.lbl_seviye.setStyleSheet("font-size: 16px; color: white; margin-left: 15px;")
        info_layout.addWidget(self.lbl_seviye)

        self.lbl_xp = QLabel("⚡ Toplam XP: 0")
        self.lbl_xp.setStyleSheet("font-size: 16px; color: #FAA2A2; margin-left: 15px;")
        info_layout.addWidget(self.lbl_xp)
        
        info_layout.addStretch()
        icerik_layout.addWidget(self.info_frame)

        self.grafik_frame = QWidget()
        self.grafik_frame.setStyleSheet("background-color: #ffffff; border-radius: 10px;")
        grafik_layout = QVBoxLayout(self.grafik_frame)

        self.lbl_resim = QLabel("Grafik Yükleniyor...")
        self.lbl_resim.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_resim.setStyleSheet("color: gray; font-size: 14px; font-style: italic;")
        grafik_layout.addWidget(self.lbl_resim)

        icerik_layout.addWidget(self.grafik_frame, stretch=1)
        ana_layout.addWidget(icerik_widget)

    def verileri_yukle(self, kullanici):
        if kullanici:
            engine = AnalyticsEngine(self.repo)
            engine.xp_liderlik_grafigi_ciz()
            
            self.lbl_isim.setText(f"Öğrenci: {kullanici.kullanici_adi}")
            self.lbl_seviye.setText(f"🏆 Seviye: {kullanici.seviye}")
            self.lbl_xp.setText(f"⚡ Toplam XP: {kullanici.toplam_xp}")
            
            try:
                pixmap = QPixmap("analiz_liderlik_tablosu.png")
                if not pixmap.isNull():
                    scaled_pixmap = pixmap.scaled(800, 500, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                    self.lbl_resim.setPixmap(scaled_pixmap)
                else:
                    self.lbl_resim.setText("Grafik oluşturuldu ama okunamadı.")
            except Exception as e:
                self.lbl_resim.setText(f"Henüz yeterli veri yok veya grafik bulunamadı.\n(Kod: {str(e)})")