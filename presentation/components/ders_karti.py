import tkinter as tk

class DersKarti(tk.Frame):
    #ridge çerçeve, 2 kalınlığında bir çerçeve çizmek için yazdım 
    def __init__(self, parent, ders_basligi, ders_turu, baslat_komutu):
        super().__init__(parent, relief="ridge", borderwidth=2, padx=10, pady=10)

        self.lbl_baslik=tk.Label(self, text=ders_basligi, font=("Arial", 12, "bold"))
        self.lbl_baslik.pack(anchor="w", pady=(0,5))

        self.lbl_turu= tk.Label(self, text=f"Tür: {ders_turu}", font=("Arial", 10), fg="gray")
        self.lbl_turu.pack(anchor="w", pady=(0,10))

        self.btn_basla=tk.Button(self, text="Dersi Başlat", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), command=baslat_komutu)
        self.btn_basla.pack(anchor="e")