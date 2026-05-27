import tkinter as tk

class GirisEkrani(tk.Frame):
    def __init__(self, parent, giris_komutu):
        super().__init__(parent, bg="#2b2b2b")
        
        # main.py'den gelecek olan doğrulama fonksiyonunu (callback) kaydediyorum
        self.giris_komutu = giris_komutu

        # Tüm bileşenleri ekranın tam ortasında tutmak için bir frame oluşturuyorum
        self.orta_panel = tk.Frame(self, bg="#2b2b2b")
        # place() ile ekranın tam ortasına x ve y ekseninde %50 (hizalıyorum
        self.orta_panel.place(relx=0.5, rely=0.5, anchor="center")

        # Başlık
        self.lbl_baslik = tk.Label(self.orta_panel, text="YazılımGo'ya Hoş Geldiniz", font=("Arial", 18, "bold"), bg="#2b2b2b", fg="#4CAF50")
        self.lbl_baslik.pack(pady=(0, 20))

        # Kullanıcı Adı Etiketi
        self.lbl_kullanici = tk.Label(self.orta_panel, text="Kullanıcı Adınızı Girin:", font=("Arial", 12), bg="#2b2b2b", fg="white")
        self.lbl_kullanici.pack(pady=(10,5))

        # Metin Kutusu (Entry)
        self.txt_kullanici = tk.Entry(self.orta_panel, font=("Arial", 14), width=20, justify="center")
        self.txt_kullanici.pack(pady=10)

        # Hata Mesajı Etiketi 
        self.lbl_hata = tk.Label(self.orta_panel, text="", font=("Arial", 10, "bold"), bg="#2b2b2b", fg="#ff4c4c")
        self.lbl_hata.pack(pady=(0, 10))

        # Giriş Butonu
        self.btn_giris = tk.Button(self.orta_panel, text="Giriş Yap", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", width=15, command=self.giris_yap_tetikle)
        self.btn_giris.pack()

    def giris_yap_tetikle(self):
        """Butona basıldığında çalışır."""
        kullanici_adi = self.txt_kullanici.get().strip()
        
        # Eğer kutu boşsa hata versin dedim
        if not kullanici_adi:
            self.lbl_hata.config(text="Kullanıcı adı boş bırakılamaz!")
            return
            
        # Boş değilse, kontrol etmesi için girilen ismi main.py'ye fırlatsın dedim
        self.giris_komutu(kullanici_adi)
        
    def hata_goster(self, mesaj):
        """Eğer main.py kullanıcıyı bulamazsa burayı tetikleyip hata mesajı gönderir."""
        self.lbl_hata.config(text=mesaj)