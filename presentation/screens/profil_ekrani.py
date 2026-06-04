import tkinter as tk
from bll.analytics_engine import AnalyticsEngine

class ProfilEkrani(tk.Frame):
    def __init__(self, parent, ana_menuye_don_komutu, kullanici_repo):
        super().__init__(parent, bg="#2b2b2b")
        self.ana_menuye_don_komutu = ana_menuye_don_komutu
        self.repo = kullanici_repo
        
        self.header_frame = tk.Frame(self, bg="#1e1e1e")
        self.header_frame.pack(fill="x", pady=10, padx=20)

        self.btn_geri = tk.Button(self.header_frame, text="⬅ Ana Menüye Dön", 
                                  command=self.ana_menuye_don_komutu, 
                                  bg="#4CAF50", fg="white", font=("DejaVu Sans", 10, "bold"))
        self.btn_geri.pack(side="left")

        self.lbl_baslik = tk.Label(self.header_frame, text="Öğrenci Profili", 
                                   font=("DejaVu Sans", 14, "bold"), bg="#1e1e1e", fg="white")
        self.lbl_baslik.pack(side="left", padx=20)

        self.info_frame = tk.Frame(self, bg="#2b2b2b")
        self.info_frame.pack(pady=10)

        self.lbl_isim = tk.Label(self.info_frame, text="Öğrenci: ...", font=("DejaVu Sans", 18, "bold"), bg="#2b2b2b", fg="#ADBB32")
        self.lbl_isim.pack(side="left", padx=15)
        
        self.lbl_seviye = tk.Label(self.info_frame, text="🏆 Seviye: 1", font=("DejaVu Sans", 14), bg="#2b2b2b", fg="white")
        self.lbl_seviye.pack(side="left", padx=15)
        
        self.lbl_xp = tk.Label(self.info_frame, text="⚡ Toplam XP: 0", font=("DejaVu Sans", 14), bg="#2b2b2b", fg="#00FF40")
        self.lbl_xp.pack(side="left", padx=15)

        self.content_frame = tk.Frame(self, bg="#ffffff", bd=2, relief="ridge")
        self.content_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        self.lbl_resim = tk.Label(self.content_frame, bg="#ffffff")
        self.lbl_resim.pack(expand=True, fill="both")
        
        self.guncel_resim = None

    def verileri_yukle(self, kullanici):
        if kullanici:
            engine = AnalyticsEngine(self.repo)
            engine.xp_liderlik_grafigi_ciz()
            
            self.lbl_isim.config(text=f"Öğrenci: {kullanici.kullanici_adi}")
            self.lbl_seviye.config(text=f"🏆 Seviye: {kullanici.seviye}")
            self.lbl_xp.config(text=f"Toplam XP: {kullanici.toplam_xp}")
            
            try:
                self.guncel_resim = tk.PhotoImage(file="analiz_liderlik_tablosu.png").subsample(2, 2)
                self.lbl_resim.config(image=self.guncel_resim)
            except Exception as e:
                self.lbl_resim.config(text="Henüz yeterli veri yok.", fg="gray")