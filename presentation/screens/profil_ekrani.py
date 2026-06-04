import tkinter as tk
from bll.analytics_engine import AnalyticsEngine

class ProfilEkrani(tk.Frame):
    def __init__(self, parent, ana_menuye_don_komutu, kullanici_repo):
        super().__init__(parent, bg="#2b2b2b")
        self.ana_menuye_don_komutu = ana_menuye_don_komutu
        self.repo=kullanici_repo
        engine=AnalyticsEngine(self.repo)
        engine.xp_liderlik_grafigi_ciz()

        self.ust_panel = tk.Frame(self, bg="#1e1e1e")
        self.ust_panel.pack(fill="x", pady=10, padx=20)

        self.btn_geri = tk.Button(self.ust_panel, text="⬅ Ana Menüye Dön", command=self.ana_menuye_don_komutu, bg="#4CAF50", fg="white", font=("DejaVu Sans", 10, "bold"))
        self.btn_geri.pack(side="left")

        self.lbl_baslik = tk.Label(self.ust_panel, text="Öğrenci Profili ve İstatistikler", font=("DejaVu Sans", 14, "bold"), bg="#1e1e1e", fg="white")
        self.lbl_baslik.pack(side="left", padx=20)

        # Bilgi
        self.bilgi_panel = tk.Frame(self, bg="#2b2b2b")
        self.bilgi_panel.pack(pady=10)

        self.lbl_isim = tk.Label(self.bilgi_panel, text="Kullanıcı: ...", font=("DejaVu Sans", 18, "bold"), bg="#2b2b2b", fg="#ADBB32")
        self.lbl_isim.pack(side="left", padx=10)

        self.lbl_seviye = tk.Label(self.bilgi_panel, text="Seviye: 1", font=("DejaVu Sans", 14), bg="#2b2b2b", fg="white")
        self.lbl_seviye.pack(side="left", padx=10)

        self.lbl_xp = tk.Label(self.bilgi_panel, text="Toplam XP: 0", font=("DejaVu Sans", 14), bg="#2b2b2b", fg="#00FF40")
        self.lbl_xp.pack(side="left", padx=10)

        # Matplotlib PNG Alanı
        self.grafik_panel = tk.Frame(self, bg="#ffffff", bd=2, relief="ridge")
        self.grafik_panel.pack(pady=10, padx=20, fill="both", expand=True)
        
        self.lbl_resim = tk.Label(self.grafik_panel, bg="#ffffff")
        self.lbl_resim.pack(expand=True)
        
        self.guncel_resim = None # Resmi RAM'de (Çöp toplayıcıdan) korumak için saklıyoruz

    def verileri_yukle(self, kullanici):
        if kullanici:
            self.lbl_isim.config(text=f"Öğrenci: {kullanici.kullanici_adi}")
            self.lbl_seviye.config(text=f"🏆 Seviye: {kullanici.seviye}")
            self.lbl_xp.config(text=f"⚡ Toplam XP: {kullanici.toplam_xp}")
            
            try:
                # Profil açıldığında Liderlik Tablosunu ekrana basar.
                # subsample(2, 2) resmi Tkinter içine sığdırmak için boyutunu yarıya indirir.
                self.guncel_resim = tk.PhotoImage(file="analiz_liderlik_tablosu.png").subsample(2,2)
                self.lbl_resim.config(image=self.guncel_resim)
            except Exception as e:
                self.lbl_resim.config(text=f"Henüz yeterli veri yok veya grafik bulunamadı.\n(Kod: {str(e)})", fg="gray", font=("DejaVu Sans", 12, "italic"))