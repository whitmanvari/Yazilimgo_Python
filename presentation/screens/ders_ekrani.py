from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTextEdit, QProgressBar)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont
import time
from bll.code_runner import CodeRunner

class KodCalistiriciThread(QThread):
    # İşlem bitince ana ekrana fırlatacağımız sinyal, İçinde string veri taşıyacak
    sonuc_sinyali = pyqtSignal(str)

    def __init__(self, code_runner, kod):
        super().__init__()
        self.code_runner = code_runner
        self.kod = kod

    def run(self):
        print("QThread başladı...")
        time.sleep(2) 
        sonuc = self.code_runner.kod_calistir(self.kod)
        self.sonuc_sinyali.emit(sonuc)

class DersEkrani(QWidget):
    def __init__(self, parent=None, ana_menuye_don_komutu=None, ders_tamamlandi_komutu=None):
        super().__init__(parent)
        self.code_runner = CodeRunner()
        self.ana_menuye_don_komutu = ana_menuye_don_komutu
        self.ders_tamamlandi_komutu = ders_tamamlandi_komutu
        self.aktif_ders = None
        self.kod_thread = None

        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("QWidget { background-color: #f5f5f5; }")
        ana_layout = QVBoxLayout(self)
        ana_layout.setContentsMargins(20, 20, 20, 20)
        ana_layout.setSpacing(15)

        header_layout = QHBoxLayout()
        
        self.btn_geri = QPushButton("⬅ Ana Menüye Dön")
        self.btn_geri.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_geri.setStyleSheet("""
            QPushButton {
                background-color: #ffffff; color: #333; font-weight: bold;
                padding: 10px 15px; border-radius: 6px; border: 1px solid #ccc;
            }
            QPushButton:hover { background-color: #e0e0e0; }
        """)
        if self.ana_menuye_don_komutu:
            self.btn_geri.clicked.connect(self.ana_menuye_don_komutu)
        header_layout.addWidget(self.btn_geri)

        self.lbl_soru = QLabel("Görev: ...")
        self.lbl_soru.setWordWrap(True) 
        self.lbl_soru.setStyleSheet("font-size: 16px; font-weight: bold; color: #333; padding-left: 20px;")
        header_layout.addWidget(self.lbl_soru, stretch=1)
        
        ana_layout.addLayout(header_layout)

        # Kod Yazma Alanı
        self.txt_kod = QTextEdit()
        font = QFont("Courier", 12) 
        self.txt_kod.setFont(font)
        self.txt_kod.setStyleSheet("""
            QTextEdit {
                background-color: #2b2b2b; color: #ffffff;
                border-radius: 8px; padding: 10px; border: 2px solid #ccc;
            }
            QTextEdit:focus { border: 2px solid #FAA2A2; }
        """)
        ana_layout.addWidget(self.txt_kod, stretch=2)

        # Terminal Çıktısı Başlığı
        self.lbl_cikti_baslik = QLabel("Terminal Çıktısı:")
        self.lbl_cikti_baslik.setStyleSheet("font-size: 14px; font-weight: bold; color: #333;")
        ana_layout.addWidget(self.lbl_cikti_baslik)

        self.txt_cikti = QTextEdit()
        self.txt_cikti.setFont(font)
        self.txt_cikti.setReadOnly(True) # Kullanıcı buraya yazı yazamaz
        self.txt_cikti.setStyleSheet("""
            QTextEdit {
                background-color: #000000; color: #FAA2A2;
                border-radius: 8px; padding: 10px;
            }
        """)
        ana_layout.addWidget(self.txt_cikti, stretch=1)

        footer_layout = QVBoxLayout()
        footer_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.progress = QProgressBar()
        self.progress.setRange(0, 0) 
        self.progress.setFixedHeight(10)
        self.progress.setStyleSheet("""
            QProgressBar { border: none; background-color: #e0e0e0; border-radius: 5px; }
            QProgressBar::chunk { background-color: #FAA2A2; border-radius: 5px; }
        """)
        self.progress.hide() # Başlangıçta gizli
        footer_layout.addWidget(self.progress)

        self.lbl_status = QLabel("Kod inceleniyor...")
        self.lbl_status.setStyleSheet("color: #666; font-style: italic;")
        self.lbl_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_status.hide()
        footer_layout.addWidget(self.lbl_status)

        self.btn_calistir = QPushButton("Kodu Çalıştır!")
        self.btn_calistir.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_calistir.setFixedWidth(200)
        self.btn_calistir.setStyleSheet("""
            QPushButton {
                background-color: #FAA2A2; color: white; font-weight: bold; font-size: 14px;
                padding: 12px; border-radius: 8px; border: none;
            }
            QPushButton:hover { background-color: #790909; }
            QPushButton:disabled { background-color: #ccc; color: #888; }
        """)
        self.btn_calistir.clicked.connect(self.kodu_calistir)
        footer_layout.addWidget(self.btn_calistir, alignment=Qt.AlignmentFlag.AlignCenter)

        self.lbl_mesaj = QLabel("")
        self.lbl_mesaj.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_mesaj.setStyleSheet("font-size: 16px; font-weight: bold;")
        footer_layout.addWidget(self.lbl_mesaj)

        ana_layout.addLayout(footer_layout)

    def aktif_dersi_ayarla(self, ders):
        self.aktif_ders = ders
        self.lbl_mesaj.setText("")
        self.lbl_soru.setText(f"Görev: {ders.soru_metni}")
        
        # Ekran her açıldığında eski kodları ve çıktıları temizle
        self.txt_kod.clear()
        self.txt_cikti.clear()

    def kodu_calistir(self):
        self.lbl_mesaj.setText("")
        self.btn_calistir.setEnabled(False)
        self.progress.show()
        self.lbl_status.show()
       
        # QTextEdit'ten metni almak için toPlainText() kullanılır
        kullanici_kodu = self.txt_kod.toPlainText()

        # Thread'i oluştur ve başlat
        self.kod_thread = KodCalistiriciThread(self.code_runner, kullanici_kodu)
        # Thread'den gelen sonucu ekrani_guncelle fonksiyonuna bağlıyorum
        self.kod_thread.sonuc_sinyali.connect(self._ekrani_guncelle)
        self.kod_thread.start()

    def _ekrani_guncelle(self, sonuc):
        # Bu fonksiyon Thread bittiğinde otomatik olarak tetiklenir
        self.txt_cikti.setText(sonuc)

        self.progress.hide()
        self.lbl_status.hide()
        self.btn_calistir.setEnabled(True)

        if self.aktif_ders and sonuc.strip() == self.aktif_ders.dogru_cevap.strip():
            self.lbl_mesaj.setStyleSheet("color: #790909; font-size: 16px; font-weight: bold;")
            self.lbl_mesaj.setText("Tebrikler! Doğru cevap.")
            if self.ders_tamamlandi_komutu:
                self.ders_tamamlandi_komutu(self.aktif_ders)
        else:
            self.lbl_mesaj.setStyleSheet("color: #d32f2f; font-size: 16px; font-weight: bold;")
            self.lbl_mesaj.setText("Tekrar dene, cevap yanlış...")