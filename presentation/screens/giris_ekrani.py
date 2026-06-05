from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtCore import Qt

class GirisEkrani(QWidget):
    def __init__(self, parent=None, giris_komutu=None, kayit_komutu=None):
        super().__init__(parent)
        self.giris_komutu = giris_komutu
        self.kayit_komutu = kayit_komutu
        self.mod_kayit_mi = False

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter) 

        self.form_container = QWidget()
        self.form_container.setFixedWidth(400)
        form_layout = QVBoxLayout(self.form_container)
        form_layout.setSpacing(15) # Elemanlar arası boşluk

        # Başlık
        self.lbl_baslik = QLabel("YazılımGo'ya Giriş Yap")
        self.lbl_baslik.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_baslik.setStyleSheet("font-size: 28px; font-weight: bold; color: #FFFFFF; font-family: cursive; margin-bottom: 20px;")
        form_layout.addWidget(self.lbl_baslik)

        # Girdi Alanları
        self.txt_kullanici = self._create_input(form_layout, "Kullanıcı Adı:")

        # Email alanını oluşturup başlangıçta gizliyorum
        self.lbl_email, self.txt_email = self._create_input_pair("E-posta Adresi:")
        form_layout.addWidget(self.lbl_email)
        form_layout.addWidget(self.txt_email)
        self.lbl_email.hide()
        self.txt_email.hide()

        self.txt_sifre = self._create_input(form_layout, "Şifre:", is_password=True)

        self.lbl_hata = QLabel("")
        self.lbl_hata.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_hata.setStyleSheet("color: #ff4c4c; font-size: 14px; font-weight: bold;")
        form_layout.addWidget(self.lbl_hata)

        self.btn_ana = QPushButton("Giriş Yap")
        self.btn_ana.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_ana.setStyleSheet("""
            QPushButton {
                background-color: #570B0B;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 12px;
                border-radius: 8px; /* Oval köşeler */
            }
            QPushButton:hover {
                background-color: #790909; /* Üzerine gelince parlar */
            }
        """)
        self.btn_ana.clicked.connect(self.islem_tetikle)
        form_layout.addWidget(self.btn_ana)

        self.btn_mod_degistir = QPushButton("Hesabın yok mu? Kayıt Ol")
        self.btn_mod_degistir.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_mod_degistir.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #F4F6F8;
                font-size: 14px;
                text-decoration: underline;
                border: none;
                margin-top: 10px;
            }
            QPushButton:hover {
                color: #FFFFFF;
            }
        """)
        self.btn_mod_degistir.clicked.connect(self.mod_degistir)
        form_layout.addWidget(self.btn_mod_degistir)

        main_layout.addWidget(self.form_container)

        self.setStyleSheet("QWidget { background-color: #2b2b2b; }")

    def _create_input(self, layout, label_text, is_password=False):
        lbl, entry = self._create_input_pair(label_text, is_password)
        layout.addWidget(lbl)
        layout.addWidget(entry)
        return entry

    def _create_input_pair(self, label_text, is_password=False):
        lbl = QLabel(label_text)
        lbl.setStyleSheet("color: white; font-size: 16px; font-family: cursive;")

        entry = QLineEdit()
        entry.setStyleSheet("""
            QLineEdit {
                font-size: 14px;
                padding: 10px;
                border: 2px solid #555555;
                border-radius: 6px;
                background-color: #1e1e1e;
                color: white;
            }
            QLineEdit:focus {
                border: 2px solid #570B0B;
            }
        """)
        if is_password:
            entry.setEchoMode(QLineEdit.EchoMode.Password)
        return lbl, entry

    def mod_degistir(self):
        self.mod_kayit_mi = not self.mod_kayit_mi
        self.lbl_hata.setText("")

        if self.mod_kayit_mi:
            self.lbl_baslik.setText("YazılımGo'ya Kayıt Ol")
            self.btn_ana.setText("Kayıt Ol")
            self.btn_mod_degistir.setText("Zaten hesabın var mı? Giriş Yap")
            self.lbl_email.show()
            self.txt_email.show()
        else:
            self.lbl_baslik.setText("YazılımGo'ya Giriş Yap")
            self.btn_ana.setText("Giriş Yap")
            self.btn_mod_degistir.setText("Hesabın yok mu? Kayıt Ol")
            self.lbl_email.hide()
            self.txt_email.hide()

    def islem_tetikle(self):
        kadi = self.txt_kullanici.text().strip()
        sifre = self.txt_sifre.text().strip()

        if not kadi or not sifre:
            self.hata_goster("Lütfen tüm alanları doldurun!")
            return

        if self.mod_kayit_mi:
            email = self.txt_email.text().strip()
            if not email:
                self.hata_goster("Lütfen e-posta adresini girin!")
                return
            if self.kayit_komutu:
                self.kayit_komutu(kadi, email, sifre)
        else:
            if self.giris_komutu:
                self.giris_komutu(kadi, sifre)

    def hata_goster(self, mesaj, basarili_mi=False):
        renk = "#EFF7EF" if basarili_mi else "#ff4c4c"
        self.lbl_hata.setStyleSheet(f"color: {renk}; font-size: 14px; font-weight: bold;")
        self.lbl_hata.setText(mesaj)