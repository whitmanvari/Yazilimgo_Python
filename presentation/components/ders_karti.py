from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt

class DersKarti(QFrame):
    def __init__(self, parent=None, baslik="", tur="", komut=None, tamamlandi_mi=False):
        super().__init__(parent)
        
        arkaplan_rengi = "#FAC0C0" if tamamlandi_mi else "#ffffff"
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {arkaplan_rengi};
                border: 1px solid #ddd;
                border-radius: 10px;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        
        self.lbl_baslik = QLabel(baslik)
        self.lbl_baslik.setStyleSheet("font-weight: bold; font-size: 18px; border: none; color: #333;")
        layout.addWidget(self.lbl_baslik)
        
        self.lbl_tur = QLabel(f"Tür: {tur}")
        self.lbl_tur.setStyleSheet("color: #666; font-style: italic; border: none; font-size: 12px;")
        layout.addWidget(self.lbl_tur)
        
        btn_renk = "#FAA2A2" if tamamlandi_mi else "#790909"
        btn_metin = "Tekrar Çöz" if tamamlandi_mi else "Derse Başla"
        
        self.btn_git = QPushButton(btn_metin)
        self.btn_git.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_git.setStyleSheet(f"""
            QPushButton {{
                background-color: {btn_renk};
                color: white;
                font-weight: bold;
                padding: 8px 20px;
                border-radius: 6px;
                border: none;
            }}
            QPushButton:hover {{ background-color: #570B0B; }}
        """)
        if komut:
            self.btn_git.clicked.connect(komut)
        
        layout.addWidget(self.btn_git, alignment=Qt.AlignmentFlag.AlignRight)