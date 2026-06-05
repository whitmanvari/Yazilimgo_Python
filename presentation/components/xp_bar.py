from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PyQt6.QtCore import Qt

class XPBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.level_label = QLabel("Seviye: 1")
        self.level_label.setStyleSheet("color: white; font-weight: bold; font-size: 16px;")
        layout.addWidget(self.level_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(18)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #555;
                border-radius: 8px;
                background-color: #444;
            }
            QProgressBar::chunk {
                background-color: #FAA2A2;
                border-radius: 7px;
            }
        """)
        layout.addWidget(self.progress_bar)

        self.xp_text = QLabel("0 / 100 XP")
        self.xp_text.setStyleSheet("color: #ccc; font-size: 12px; font-weight: bold;")
        self.xp_text.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.xp_text)

    def guncelle(self, mevcut_xp, seviye, seviye_siniri=100):
        self.level_label.setText(f"Seviye: {seviye}")
        self.xp_text.setText(f"{mevcut_xp % seviye_siniri} / {seviye_siniri} XP")
        ilerleme_yuzdesi = int(((mevcut_xp % seviye_siniri) / seviye_siniri) * 100)
        self.progress_bar.setValue(ilerleme_yuzdesi)