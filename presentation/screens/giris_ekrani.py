import tkinter as tk

class GirisEkrani(tk.Frame):
    def __init__(self, parent, giris_komutu, kayit_komutu):
        super().__init__(parent, bg="#2b2b2b")
        
        self.giris_komutu = giris_komutu
        self.kayit_komutu = kayit_komutu
        self.mod_kayit_mi = False # Başlangıçta giriş modunda başlar

        self.orta_panel = tk.Frame(self, bg="#2b2b2b")
        self.orta_panel.place(relx=0.5, rely=0.5, anchor="center")

        self.lbl_baslik = tk.Label(self.orta_panel, text="YazılımGo'ya Giriş Yap", font=("Arial", 18, "bold"), bg="#2b2b2b", fg="#4CAF50")
        self.lbl_baslik.pack(pady=(0, 20))

        # Kullanıcı Adı
        self.lbl_kullanici = tk.Label(self.orta_panel, text="Kullanıcı Adı:", font=("Arial", 12), bg="#2b2b2b", fg="white")
        self.lbl_kullanici.pack(anchor="w")
        self.txt_kullanici = tk.Entry(self.orta_panel, font=("Arial", 14), width=25)
        self.txt_kullanici.pack(pady=(0, 10))

        # E-posta (Sadece Kayıt modunda görünür, başlangıçta gizli)
        self.lbl_email = tk.Label(self.orta_panel, text="E-posta Adresi:", font=("Arial", 12), bg="#2b2b2b", fg="white")
        self.txt_email = tk.Entry(self.orta_panel, font=("Arial", 14), width=25)
        
        # Şifre
        self.lbl_sifre = tk.Label(self.orta_panel, text="Şifre:", font=("Arial", 12), bg="#2b2b2b", fg="white")
        self.lbl_sifre.pack(anchor="w")
        self.txt_sifre = tk.Entry(self.orta_panel, font=("Arial", 14), width=25, show="*") # Yıldızlı gösterim
        self.txt_sifre.pack(pady=(0, 15))

        self.lbl_hata = tk.Label(self.orta_panel, text="", font=("Arial", 10, "bold"), bg="#2b2b2b", fg="#ff4c4c")
        self.lbl_hata.pack(pady=(0, 10))

        self.btn_ana = tk.Button(self.orta_panel, text="Giriş Yap", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", width=20, command=self.islem_tetikle)
        self.btn_ana.pack(pady=5)

        # Mod Değiştirme Linki (Giriş <-> Kayıt)
        self.btn_mod_degistir = tk.Button(self.orta_panel, text="Hesabın yok mu? Kayıt Ol", font=("Arial", 10, "underline"), bg="#2b2b2b", fg="#2196F3", bd=0, activebackground="#2b2b2b", cursor="hand2", command=self.mod_degistir)
        self.btn_mod_degistir.pack(pady=10)

    def mod_degistir(self):
        """Kayıt ve Giriş modları arasında ekranı günceller."""
        self.mod_kayit_mi = not self.mod_kayit_mi
        self.lbl_hata.config(text="") 
        
        if self.mod_kayit_mi:
            self.lbl_baslik.config(text="YazılımGo'ya Kayıt Ol")
            self.btn_ana.config(text="Kayıt Ol")
            self.btn_mod_degistir.config(text="Zaten hesabın var mı? Giriş Yap")
            
            # E-posta alanını araya sıkıştırmak için diğerlerini geçici olarak gizleyip yeniden diziyoruz
            self.lbl_sifre.pack_forget()
            self.txt_sifre.pack_forget()
            self.lbl_hata.pack_forget()
            self.btn_ana.pack_forget()
            self.btn_mod_degistir.pack_forget()
            
            self.lbl_email.pack(anchor="w")
            self.txt_email.pack(pady=(0, 10))
            self.lbl_sifre.pack(anchor="w")
            self.txt_sifre.pack(pady=(0, 15))
            self.lbl_hata.pack(pady=(0, 10))
            self.btn_ana.pack(pady=5)
            self.btn_mod_degistir.pack(pady=10)
        else:
            self.lbl_baslik.config(text="YazılımGo'ya Giriş Yap")
            self.btn_ana.config(text="Giriş Yap")
            self.btn_mod_degistir.config(text="Hesabın yok mu? Kayıt Ol")
            self.lbl_email.pack_forget()
            self.txt_email.pack_forget()

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
        renk = "#4CAF50" if basarili_mi else "#ff4c4c"
        self.lbl_hata.config(text=mesaj, fg=renk)