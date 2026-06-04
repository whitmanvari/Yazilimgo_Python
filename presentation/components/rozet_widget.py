import tkinter as tk

class RozetWidget(tk.Frame):
    def __init__(self, pencere, bg="#ffffff"):
        super().__init__(pencere, bg=bg)
        self.bg = bg

        self.baslik = tk.Label(self, text="Kazanılan Rozetler", font=("DejaVu Sans", 12, "bold"), bg=bg)
        self.baslik.pack(anchor="w", pady=(0, 10))

        self.rozet_alani = tk.Frame(self, bg=bg)
        self.rozet_alani.pack(fill="both", expand=True)

    def rozetleri_goster(self, rozet_listesi):
        # Eski rozetleri temizle
        for widget in self.rozet_alani.winfo_children():
            widget.destroy()

        if not rozet_listesi:
            tk.Label(self.rozet_alani, text="Henüz hiç rozet kazanılmadı.", 
                     fg="gray", font=("DejaVu Sans", 10, "italic"), bg=self.bg).pack(anchor="w")
            return

        for i, rozet_adi in enumerate(rozet_listesi):
            satir = i // 4
            sutun = i % 4
            
            kart = tk.Frame(self.rozet_alani, bg="#ffffff", bd=1, relief="ridge", padx=10, pady=10)
            kart.grid(row=satir, column=sutun, padx=10, pady=10)

            tk.Label(kart, text="🎖️", font=("DejaVu Sans", 32), bg="#ffffff").pack()
            tk.Label(kart, text=rozet_adi, font=("DejaVu Sans", 10, "bold"), 
                     bg="#ffffff", fg="#333333").pack(pady=(5,0))