import tkinter as tk

class SidebarWidget(tk.Frame):
    def __init__(self, parent, sayfa_gecis_komutu, cikis_komutu):
        super().__init__(parent, bg="#1e1e1e")
        self.pack_propagate(False) 

        self.sayfa_gecis_komutu = sayfa_gecis_komutu
        self.cikis_komutu = cikis_komutu

        self.kapali_genislik = 50
        self.acik_genislik = 200
        self.hedef_genislik = self.kapali_genislik
        self.animasyon_id = None

        self.btn_hamburger = tk.Label(self, text="☰", font=("DejaVu Sans", 14), bg="#1e1e1e", fg="white", cursor="hand2")
        self.btn_hamburger.pack(anchor="nw", padx=12, pady=10)

        self.lbl_logo = tk.Label(self, text="YazılımGo", font=("cursive", 18), bg="#1e1e1e", fg="white")

        # Buton Verilerimiz
        self.buton_verileri = [
            {"text": "Dersler", "komut": lambda: self.sayfa_gecis_komutu("AnaMenu"), "alt": False, "renk": "#1e1e1e"},
            {"text": "Rozetler", "komut": lambda: self.sayfa_gecis_komutu("KazanimlarEkrani"), "alt": False, "renk": "#1e1e1e"},
            {"text": "Profil", "komut": lambda: self.sayfa_gecis_komutu("ProfilEkrani"), "alt": False, "renk": "#1e1e1e"},
            {"text": "Çıkış Yap", "komut": self.cikis_komutu, "alt": True, "renk": "#680b0b"}
        ]

        self.butonlar = []

        for veri in self.buton_verileri:
            btn = tk.Button(self, text=veri["text"], command=veri["komut"],
                            bg=veri["renk"], fg="white", font=("DejaVu Sans", 11),
                            bd=0, anchor="w", padx=15, pady=10, 
                            activebackground="#555555", activeforeground="white",
                            highlightthickness=0) 
            
            btn.bind("<Enter>", lambda e, b=btn: self._btn_hover_gir(e, b))
            btn.bind("<Leave>", lambda e, b=btn, r=veri["renk"]: self._btn_hover_cik(e, b, r))
            self.butonlar.append(btn)

        self.bind("<Enter>", self.genislet)
        self.bind("<Leave>", self.daralt)
        self.btn_hamburger.bind("<Enter>", self.genislet)

    def _btn_hover_gir(self, event, btn):
        self.genislet() # Hover durumunda menünün kapanmasını engeller
        btn.config(bg="#444444") # Hover rengi

    def _btn_hover_cik(self, event, btn, orijinal_renk):
        btn.config(bg=orijinal_renk)

    def genislet(self, event=None):
        if self.hedef_genislik == self.acik_genislik:
            return # Zaten açıksa tekrar işlem yapma

        self.hedef_genislik = self.acik_genislik
        
        
        self.lbl_logo.pack(fill="x", pady=(0, 20))
        for i, btn in enumerate(self.butonlar):
            if self.buton_verileri[i]["alt"]:
                btn.pack(side="bottom", fill="x", pady=10)
            else:
                btn.pack(fill="x", pady=5)
                
        self._animasyon()

    def daralt(self, event=None):
        if self.hedef_genislik == self.kapali_genislik:
            return # Zaten kapalıysa tekrar işlem yapma

        self.hedef_genislik = self.kapali_genislik
        
        self.lbl_logo.pack_forget()
        for btn in self.butonlar:
            btn.pack_forget()
            
        self._animasyon()

    def _animasyon(self):
        try:
            mevcut = int(self.place_info().get('width', self.winfo_width()))
        except:
            mevcut = self.winfo_width()
            
        adim = 30 # Animasyon hızı 
        
        if self.animasyon_id:
            self.after_cancel(self.animasyon_id)

        if mevcut < self.hedef_genislik:
            yeni = min(mevcut + adim, self.hedef_genislik)
            self.place_configure(width=yeni)
            self.animasyon_id = self.after(10, self._animasyon)
        elif mevcut > self.hedef_genislik:
            yeni = max(mevcut - adim, self.hedef_genislik)
            self.place_configure(width=yeni)
            self.animasyon_id = self.after(10, self._animasyon)