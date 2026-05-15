import tkinter as tk
from entities import kazanim
from presentation.components.xp_bar import XPBar
from presentation.components.rozet_widget import RozetWidget
from presentation.components.ders_karti import DersKarti

class AnaMenuEkrani(tk.Frame):
    def __init__(self, parent,kullanici_servisi, ders_servisi):
        super().__init__(parent)

        self.kullanici_servisi=kullanici_servisi
        self.ders_servisi=ders_servisi

        self.aktif_kullanici_id=1

        self.sol_panel=tk.Frame(self, width=250, bg='#2b2b2b')
        self.sol_panel.pack(side="left", fill="y")

        self.sag_panel=tk.Frame(self, bg="#ffffff")
        self.sag_panel.pack(side="right", fill="both", expand=True)

        self.xp_bar = XPBar(self.sol_panel)
        self.xp_bar.pack(pady=10, padx=10, fill="x")

        self.rozet_widget= RozetWidget(self.sol_panel)
        self.rozet_widget.pack(pady=20, padx=10, fill="x")

        self.lbl_dersler=tk.Label(self.sag_panel, text="Mevcut Dersler", font=("Arial", 12, "bold"), bg="#ffffff")
        self.lbl_dersler.pack(pady=20, padx=10, anchor="w")

        self.ders_listesi_frame= tk.Frame(self,self.sag_panel, bg="#ffffff")
        self.ders_listesi_frame.pack(fill="both", expand=True, padx=20)

    def verileri_yukle(self):
        kullanici=self.kullanici_servisi.repo.id_ile_getir(self.aktif_kullanici_id)
        if kullanici:
            self.xp_bar.guncelle(kullanici.toplam_xp, kullanici.seviye)
            rozetler=[]
            for k in kullanici.kazanimlar:
                rozetler.append(kazanim.kazanim.kazanim_adi)

            self.rozet_widget.rozetleri_goster(rozetler)
        dersler = self.ders_servisi.modulun_derslerini_getir(modul_id=1)
        if dersler:
            for ders in dersler:
                kart = DersKarti(
                    self.ders_listesi_frame,
                    ders.ders_basligi,
                    ders.ders_turu,
                    lambda d= ders: self.dersi_baslat(d)
                )
                kart.pack(pady=5, fill="x")

    def dersi_baslat(self, ders):
        print(f"{ders.ders_basligi} ekranına geçiliyor...")