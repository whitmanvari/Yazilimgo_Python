import tkinter as tk

class KazanimlarEkrani(tk.Frame):
    def __init__(self, parent, ana_menuye_don_komutu):
        super().__init__(parent, bg="#ffffff")
        self.ana_menuye_don_komutu = ana_menuye_don_komutu

        # Üst Panel
        self.ust_panel = tk.Frame(self, bg="#4CAF50")
        self.ust_panel.pack(fill="x")

        self.btn_geri = tk.Button(self.ust_panel, text="⬅ Ana Menüye Dön", command=self.ana_menuye_don_komutu, bg="#388E3C", fg="white", font=("DejaVu Sans", 10, "bold"), bd=0, padx=10, pady=10)
        self.btn_geri.pack(side="left")

        self.lbl_baslik = tk.Label(self.ust_panel, text="Kazandığın Rozetler", font=("DejaVu Sans", 14, "bold"), bg="#4CAF50", fg="white")
        self.lbl_baslik.pack(side="left", padx=20, pady=10)

        # Rozetlerin dizileceği ana alan olacak
        self.rozetler_alani = tk.Frame(self, bg="#ffffff")
        self.rozetler_alani.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Eğer hiç rozet yoksa görünecek mesajı yazdım
        self.lbl_bos_mesaj = tk.Label(self.rozetler_alani, text="Henüz hiç rozet kazanmadın.\nDersleri tamamlayarak rozet kazanabilirsin!", font=("DejaVu Sans", 12, "italic"), bg="#ffffff", fg="#666666")

    def verileri_yukle(self, kazanimlar):
        """Kullanıcının kazandığı rozetleri ekrana dizer."""
        # Önce eski rozetleri temizleyelim
        for widget in self.rozetler_alani.winfo_children():
            widget.destroy()

        if not kazanimlar or len(kazanimlar) == 0:
            # Liste boşsa mesajı göstersin
            self.lbl_bos_mesaj = tk.Label(self.rozetler_alani, text="Henüz hiç rozet kazanmadın.\nDersleri tamamlayarak rozet kazanabilirsin!", font=("DejaVu Sans", 12, "italic"), bg="#ffffff", fg="#666666")
            self.lbl_bos_mesaj.pack(pady=50)
            return

        # Rozetleri Grid  mantığıyla yan yana dizdim
        satir = 0
        sutun = 0
        for kazanim in kazanimlar:
            # Rozet Kartı
            kart = tk.Frame(self.rozetler_alani, bg="#ffffff", bd=1, relief="ridge", padx=10, pady=10)
            kart.grid(row=satir, column=sutun, padx=10, pady=10)

            # Rozet İkonu 
            ikon = tk.Label(kart, text="🎖️", font=("DejaVu Sans", 32), bg="#ffffff")
            ikon.pack()

            # Rozet Adı
            isim = tk.Label(kart, text=kazanim.kazanim_adi, font=("DejaVu Sans", 12, "bold"), bg="#f9f9f9", fg="#333333")
            isim.pack(pady=(5,0))
            
            #Her satırda 4 rozet olsun
            sutun += 1
            if sutun > 3:
                sutun = 0
                satir += 1