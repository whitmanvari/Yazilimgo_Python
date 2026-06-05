import tkinter as tk
from presentation.components.rozet_widget import RozetWidget

class KazanimlarEkrani(tk.Frame):
    def __init__(self, parent, ana_menuye_don_komutu):
        super().__init__(parent, bg="#ffffff")
        self.ana_menuye_don_komutu = ana_menuye_don_komutu

        # Başlık Bölgesi
        self.header_frame = tk.Frame(self, bg="#FD9E9E")
        self.header_frame.pack(fill="x")

        self.btn_geri = tk.Button(self.header_frame, text="⬅ Ana Menüye Dön", 
                                  command=self.ana_menuye_don_komutu, 
                                  bg="#FD9E9E", fg="white", font=("DejaVu Sans", 10, "bold"), 
                                  bd=0, padx=10, pady=10)
        self.btn_geri.pack(side="left")

        self.lbl_baslik = tk.Label(self.header_frame, text="Kazandığın Rozetler", 
                                   font=("cursive", 14, "bold"), bg="#FD9E9E", fg="white")
        self.lbl_baslik.pack(side="left", padx=20, pady=10)

        self.content_frame = tk.Frame(self, bg="#ffffff")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.rozet_widget = RozetWidget(self.content_frame, bg="#ffffff")
        self.rozet_widget.pack(fill="both", expand=True)

    def verileri_yukle(self, kazanimlar):
        """Veriyi widget'a pasla, gerisine karışma!"""
        rozet_isimleri = [k.kazanim_adi for k in kazanimlar]
        self.rozet_widget.rozetleri_goster(rozet_isimleri)