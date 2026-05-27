import tkinter as tk

class ProfilEkrani(tk.Frame):
    def __init__(self, parent, ana_menuye_don_komutu):
        super().__init__(parent, bg="#2b2b2b")
        self.ana_menuye_don_komutu = ana_menuye_don_komutu

        # Üst Panel -> Geri Butonu ve Başlık
        self.ust_panel = tk.Frame(self, bg="#1e1e1e")
        self.ust_panel.pack(fill="x", pady=10, padx=20)

        self.btn_geri = tk.Button(self.ust_panel, text="⬅ Ana Menüye Dön", command=self.ana_menuye_don_komutu, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        self.btn_geri.pack(side="left")

        self.lbl_baslik = tk.Label(self.ust_panel, text="Öğrenci Profili", font=("Arial", 14, "bold"), bg="#1e1e1e", fg="white")
        self.lbl_baslik.pack(side="left", padx=20)

        # Profil Detayları Ortada (Ortalamak için place kullandım)
        self.orta_panel = tk.Frame(self, bg="#2b2b2b")
        self.orta_panel.place(relx=0.5, rely=0.5, anchor="center")

        self.lbl_isim = tk.Label(self.orta_panel, text="Kullanıcı: ...", font=("Arial", 22, "bold"), bg="#2b2b2b", fg="#4CAF50")
        self.lbl_isim.pack(pady=10)

        self.lbl_seviye = tk.Label(self.orta_panel, text="Seviye: 1", font=("Arial", 16), bg="#2b2b2b", fg="white")
        self.lbl_seviye.pack(pady=5)

        self.lbl_xp = tk.Label(self.orta_panel, text="Toplam XP: 0", font=("Arial", 16), bg="#2b2b2b", fg="#FFD700")
        self.lbl_xp.pack(pady=5)

    def verileri_yukle(self, kullanici):
        """Bu sayfaya geçildiğinde main.py tarafından tetiklenip güncel veriyi basar."""
        if kullanici:
            self.lbl_isim.config(text=f"Öğrenci: {kullanici.kullanici_adi}")
            self.lbl_seviye.config(text=f"Seviye: {kullanici.seviye}")
            self.lbl_xp.config(text=f"Toplam XP: {kullanici.toplam_xp}")