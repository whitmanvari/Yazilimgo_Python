from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from presentation.components.rozet_widget import RozetWidget

class KazanimlarEkrani(QWidget):
    def __init__(self, parent=None, ana_menuye_don_komutu=None):
        super().__init__(parent)
        self.ana_menuye_don_komutu = ana_menuye_don_komutu
        
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("QWidget { background-color: #ffffff; }")
        
        ana_layout = QVBoxLayout(self)
        ana_layout.setContentsMargins(0, 0, 0, 0) # Kenar boşluklarını sıfırla ki header uçtan uca gitsin
        ana_layout.setSpacing(0)
        
        self.header_frame = QWidget()
        self.header_frame.setStyleSheet("background-color: #FD9E9E;")
        self.header_frame.setFixedHeight(60) # Header yüksekliğini sabitliyoruz
        
        header_layout = QHBoxLayout(self.header_frame)
        header_layout.setContentsMargins(15, 0, 20, 0)
        
        self.btn_geri = QPushButton("⬅ Ana Menüye Dön")
        self.btn_geri.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_geri.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                font-family: 'DejaVu Sans';
                font-weight: bold;
                font-size: 14px;
                border: none;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #e68e8e; /* Üzerine gelince hafif koyulaşır */
                border-radius: 5px;
            }
        """)
        if self.ana_menuye_don_komutu:
            self.btn_geri.clicked.connect(self.ana_menuye_don_komutu)
        header_layout.addWidget(self.btn_geri)
        
        # Başlık Yazısı
        self.lbl_baslik = QLabel("Kazandığın Rozetler")
        self.lbl_baslik.setStyleSheet("font-family: cursive; font-size: 20px; font-weight: bold; color: white;")
        header_layout.addWidget(self.lbl_baslik)
        
        header_layout.addStretch() 
        
        ana_layout.addWidget(self.header_frame)
        
        self.content_frame = QWidget()
        content_layout = QVBoxLayout(self.content_frame)
        content_layout.setContentsMargins(30, 30, 30, 30) 
        
        self.rozet_widget = RozetWidget()
        content_layout.addWidget(self.rozet_widget)
        
        ana_layout.addWidget(self.content_frame)

    def verileri_yukle(self, kazanimlar):
        """Veriyi widget'a pasla, gerisine karışma!"""
        rozet_isimleri = []
        if kazanimlar:
            if hasattr(kazanimlar[0], 'kazanim_tanimi'):
                rozet_isimleri = [k.kazanim_tanimi.kazanim_adi for k in kazanimlar]
            elif isinstance(kazanimlar[0], str):
                rozet_isimleri = kazanimlar
                
        self.rozet_widget.rozetleri_goster(rozet_isimleri)