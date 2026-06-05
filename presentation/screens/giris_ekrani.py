import tkinter as tk

class GirisEkrani(tk.Frame):
    def __init__(self, parent, giris_komutu, kayit_komutu):
        super().__init__(parent, bg="#2b2b2b")
        
        self.giris_komutu = giris_komutu
        self.kayit_komutu = kayit_komutu
        self.mod_kayit_mi = False

        self.main_container = tk.Frame(self, bg="#2b2b2b")
        self.main_container.pack(expand=True)

        self.header_frame = tk.Frame(self.main_container, bg="#2b2b2b")
        self.header_frame.pack(pady=(0, 30))
        self.lbl_baslik = tk.Label(self.header_frame, text="YazılımGo'ya Giriş Yap", font=("cursive", 24, "bold"), bg="#2b2b2b", fg="#FFFFFF")
        self.lbl_baslik.pack()

        self.input_frame = tk.Frame(self.main_container, bg="#2b2b2b")
        self.input_frame.pack(pady=15)

        self.txt_kullanici = self._create_input("Kullanıcı Adı:")
        self.txt_email = self._create_input("E-posta Adresi:", visible=False)
        self.txt_sifre = self._create_input("Şifre:", is_password=True)

        self.footer_frame = tk.Frame(self.main_container, bg="#2b2b2b")
        self.footer_frame.pack(pady=25)
        
        self.lbl_hata = tk.Label(self.footer_frame, text="", font=("DejaVu Sans", 12), bg="#2b2b2b", fg="#570B0B")
        self.lbl_hata.pack(pady=(0, 10))

        self.btn_ana = tk.Button(self.footer_frame, text="Giriş Yap", font=("DejaVu Sans", 14, "bold"), bg="#570B0B", fg="white", width=22, pady=5, command=self.islem_tetikle)
        self.btn_ana.pack(pady=10)

        self.btn_mod_degistir = tk.Button(self.footer_frame, text="Hesabın yok mu? Kayıt Ol", font=("DejaVu Sans", 12, "underline"), bg="#2b2b2b", fg="#F4F6F8", bd=0, cursor="hand2", command=self.mod_degistir)
        self.btn_mod_degistir.pack(pady=10)

    def _create_input(self, label_text, is_password=False, visible=True):
        frame = tk.Frame(self.input_frame, bg="#2b2b2b")
        if visible: 
            frame.pack(fill="x", pady=10)
        else: 
            frame.pack_forget()
        
        tk.Label(frame, text=label_text, font=("cursive", 16), bg="#2b2b2b", fg="white").pack(anchor="w", pady=(0, 5))
        entry = tk.Entry(frame, font=("DejaVu Sans", 14), width=30, show="*" if is_password else "")
        entry.pack(fill="x", ipady=5)
        frame.label_text = label_text 
        entry.container = frame 
        return entry

    def mod_degistir(self):
        self.mod_kayit_mi = not self.mod_kayit_mi
        self.lbl_hata.config(text="")
        
        if self.mod_kayit_mi:
            self.lbl_baslik.config(text="YazılımGo'ya Kayıt Ol")
            self.btn_ana.config(text="Kayıt Ol")
            self.btn_mod_degistir.config(text="Zaten hesabın var mı? Giriş Yap")
            self.txt_email.container.pack(fill="x", pady=10, before=self.txt_sifre.container)
        else:
            self.lbl_baslik.config(text="YazılımGo'ya Giriş Yap")
            self.btn_ana.config(text="Giriş Yap")
            self.btn_mod_degistir.config(text="Hesabın yok mu? Kayıt Ol")
            self.txt_email.container.pack_forget()

    def islem_tetikle(self):
        kadi = self.txt_kullanici.get().strip()
        sifre = self.txt_sifre.get().strip()
        
        if not kadi or not sifre:
            self.hata_goster("Lütfen tüm alanları doldurun!")
            return
            
        if self.mod_kayit_mi:
            email = self.txt_email.get().strip()
            if not email:
                self.hata_goster("Lütfen e-posta adresini girin!")
                return
            self.kayit_komutu(kadi, email, sifre)
        else:
            self.giris_komutu(kadi, sifre)

    def hata_goster(self, mesaj, basarili_mi=False):
        renk = "#EFF7EF" if basarili_mi else "#570B0B"
        self.lbl_hata.config(text=mesaj, fg=renk)