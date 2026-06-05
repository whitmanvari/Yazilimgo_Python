from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSizePolicy
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve

class SidebarWidget(QWidget):
    def __init__(self, parent=None, sayfa_gecis_komutu=None, cikis_komutu=None):
        super().__init__(parent)
        self.sayfa_gecis_komutu = sayfa_gecis_komutu
        self.cikis_komutu = cikis_komutu

        self.kapali_genislik = 50
        self.acik_genislik = 200
        
        self.setFixedWidth(self.kapali_genislik)
        self.setStyleSheet("QWidget { background-color: #1e1e1e; }")

        self.init_ui()

    def init_ui(self):
        # Ana Layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 10, 0, 10)
        self.layout.setSpacing(5)

        self.btn_hamburger = QLabel("☰")
        self.btn_hamburger.setStyleSheet("font-size: 24px; color: white; padding-left: 15px;")
        self.layout.addWidget(self.btn_hamburger)

        self.lbl_logo = QLabel("")
        self.lbl_logo.setStyleSheet("font-family: cursive; font-size: 22px; font-weight: bold; color: white; padding-left: 15px;")
        self.layout.addWidget(self.lbl_logo)
        self.layout.addSpacing(20)

        self.buton_verileri = [
            {"text": "Dersler", "komut": lambda: self.sayfa_gecis_komutu("AnaMenu"), "renk": "#1e1e1e"},
            {"text": "Rozetler", "komut": lambda: self.sayfa_gecis_komutu("KazanimlarEkrani"), "renk": "#1e1e1e"},
            {"text": "Profil", "komut": lambda: self.sayfa_gecis_komutu("ProfilEkrani"), "renk": "#1e1e1e"}
        ]

        self.butonlar = []

        for veri in self.buton_verileri:
            btn = QPushButton("") # Başlangıçta metinsiz
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #1e1e1e; color: white;
                    text-align: left; padding: 12px 15px;
                    font-size: 14px; font-weight: bold; border: none;
                }
                QPushButton:hover { background-color: #444444; }
            """)
            btn.clicked.connect(veri["komut"])
            self.layout.addWidget(btn)
            self.butonlar.append((btn, veri["text"])) # Referans için tuple olarak sakla

        self.layout.addStretch() 

        # 4. Çıkış Yap Butonu (En altta)
        self.btn_cikis = QPushButton("")
        self.btn_cikis.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_cikis.setStyleSheet("""
            QPushButton {
                background-color: #680b0b; color: white;
                text-align: left; padding: 12px 15px;
                font-size: 14px; font-weight: bold; border: none;
            }
            QPushButton:hover { background-color: #8b0e0e; }
        """)
        self.btn_cikis.clicked.connect(self.cikis_komutu)
        self.layout.addWidget(self.btn_cikis)
        self.butonlar.append((self.btn_cikis, "Çıkış Yap"))

    
    def enterEvent(self, event):
        """Fare Sidebar'ın üzerine geldiğinde (Hover)"""
        self.lbl_logo.setText("YazılımGo")
        for btn, text in self.butonlar:
            btn.setText(text) # Metinleri geri getir
        self.animasyon_tetikle(self.acik_genislik)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Fare Sidebar'dan çıktığında"""
        self.lbl_logo.setText("")
        for btn, text in self.butonlar:
            btn.setText("") 
        self.animasyon_tetikle(self.kapali_genislik)
        super().leaveEvent(event)

    def animasyon_tetikle(self, hedef_genislik):
        """Yumuşak Çekmece Animasyonu"""
        self.anim_min = QPropertyAnimation(self, b"minimumWidth")
        self.anim_min.setDuration(250) # Çeyrek saniye
        self.anim_min.setStartValue(self.width())
        self.anim_min.setEndValue(hedef_genislik)
        self.anim_min.setEasingCurve(QEasingCurve.Type.InOutQuart) 
        self.anim_min.start()

        self.anim_max = QPropertyAnimation(self, b"maximumWidth")
        self.anim_max.setDuration(250)
        self.anim_max.setStartValue(self.width())
        self.anim_max.setEndValue(hedef_genislik)
        self.anim_max.setEasingCurve(QEasingCurve.Type.InOutQuart)
        self.anim_max.start()