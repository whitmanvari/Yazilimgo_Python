from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QFrame
from PyQt6.QtCore import Qt

class RozetWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.baslik = QLabel("Kazanılan Rozetler")
        self.baslik.setStyleSheet("color: white; font-weight: bold; font-size: 16px;")
        self.layout.addWidget(self.baslik)

        self.rozet_alani = QWidget()
        self.rozet_layout = QGridLayout(self.rozet_alani)
        self.rozet_layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.rozet_alani)

    def rozetleri_goster(self, rozet_listesi):
        # Eski rozetleri temizle
        for i in reversed(range(self.rozet_layout.count())): 
            widget = self.rozet_layout.itemAt(i).widget()
            self.rozet_layout.removeWidget(widget)
            widget.setParent(None)

        if not rozet_listesi:
            lbl = QLabel("Henüz hiç rozet kazanılmadı.")
            lbl.setStyleSheet("color: #ccc; font-style: italic;")
            self.rozet_layout.addWidget(lbl, 0, 0)
            return

        for i, rozet_adi in enumerate(rozet_listesi):
            satir, sutun = divmod(i, 3) # 3 sütunlu ızgara

            kart = QFrame()
            kart.setStyleSheet("background-color: white; border-radius: 8px;")
            kart_layout = QVBoxLayout(kart)

            ikon = QLabel("🎖️")
            ikon.setAlignment(Qt.AlignmentFlag.AlignCenter)
            ikon.setStyleSheet("font-size: 28px;")
            kart_layout.addWidget(ikon)

            isim = QLabel(rozet_adi)
            isim.setAlignment(Qt.AlignmentFlag.AlignCenter)
            isim.setStyleSheet("color: black; font-size: 11px; font-weight: bold;")
            kart_layout.addWidget(isim)

            self.rozet_layout.addWidget(kart, satir, sutun)