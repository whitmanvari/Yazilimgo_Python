import tkinter as tk
from tkinter import ttk #(themed tkinter) progressbar için çektim

class XPBar(tk.Frame):
    #pencere kutuyu nereye ekleyeceğimi belirtsin 
    def __init__(self, pencere):
        super().__init__(pencere)

        self.level_label=tk.Label(self, text="Seviye: 1", font=("DejaVu Sans", 12, "bold"))
        self.level_label.pack(anchor="w", padx=5)

        self.progress_bar= ttk.Progressbar(self, orient="horizontal", length=200, mode="determinate")
        self.progress_bar.pack(fill="x", padx=5, pady=2)

        self.xp_text=tk.Label(self, text="0 / 100 XP", font=("DejaVu Sans", 10))
        self.xp_text.pack(anchor="e", padx=5)

    def guncelle(self, mevcut_xp, seviye, seviye_siniri=100):
        self.level_label.config(text=f"Seviye: {seviye}")
        self.xp_text.config(text=f"{mevcut_xp % seviye_siniri} / {seviye_siniri} XP")

        #barın doluluk yüzdesi hesaplayıp güncelleme 0-100 arası
        ilerleme_yuzdesi=((mevcut_xp % seviye_siniri) / seviye_siniri) * 100
        self.progress_bar["value"] = ilerleme_yuzdesi