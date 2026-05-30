import tkinter as tk

class DersKarti(tk.Frame):
    def __init__(self, parent, ders_basligi, ders_turu, baslat_komutu, tamamlandi_mi=False):
        # Eğer ders tamamlandıysa arka planı hafif yeşil, buton rengini soluk yeşil yapıyoruz
        bg_color = "#e8f5e9" if tamamlandi_mi else "#ffffff"
        btn_color = "#81c784" if tamamlandi_mi else "#4CAF50"
        btn_text = "Tekrar Çöz" if tamamlandi_mi else "Dersi Başlat"

        super().__init__(parent, relief="ridge", borderwidth=2, padx=10, pady=10, bg=bg_color)

        self.lbl_baslik=tk.Label(self, text=ders_basligi, font=("Arial", 12, "bold"), bg=bg_color)
        self.lbl_baslik.pack(anchor="w", pady=(0,5))

        self.lbl_turu= tk.Label(self, text=f"Tür: {ders_turu}", font=("Arial", 10), fg="gray", bg=bg_color)
        self.lbl_turu.pack(anchor="w", pady=(0,10))

        self.btn_basla=tk.Button(self, text=btn_text, bg=btn_color, fg="white", font=("Arial", 10, "bold"), command=baslat_komutu)
        self.btn_basla.pack(anchor="e")