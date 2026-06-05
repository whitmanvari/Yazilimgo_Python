import tkinter as tk

class DersKarti(tk.Frame):
    def __init__(self, parent, baslik, tur, komut, tamamlandi_mi=False):
        # 1. Arka plan renkleri: Tamamlandıysa hafif pembe, tamamlanmadıysa beyaz
        arkaplan_rengi = "#FAC0C0" if tamamlandi_mi else "#ffffff"
        
        super().__init__(parent, bg=arkaplan_rengi, bd=1, relief="ridge")

        self.lbl_baslik = tk.Label(self, text=baslik, font=("DejaVu Sans", 11, "bold"), bg=arkaplan_rengi, fg="#333333")
        self.lbl_baslik.pack(anchor="w", padx=15, pady=(15, 5))

        self.lbl_tur = tk.Label(self, text=f"Tür: {tur}", font=("DejaVu Sans", 9, "italic"), bg=arkaplan_rengi, fg="#888888")
        self.lbl_tur.pack(anchor="w", padx=15, pady=(0, 10))

        btn_renk = "#FAA2A2" if tamamlandi_mi else "#790909"
        btn_metin = "Tekrar Çöz" if tamamlandi_mi else "Derse Başla"
        
        self.btn_git = tk.Button(
            self, 
            text=btn_metin, 
            bg=btn_renk, 
            fg="#ffffff", 
            font=("DejaVu Sans", 9, "bold"), 
            bd=0, 
            padx=15, 
            pady=5, 
            cursor="hand2",
            command=komut
        )
        
        self.btn_git.place(relx=1.0, rely=1.0, anchor="se", x=-15, y=-15)