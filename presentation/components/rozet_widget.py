import tkinter as tk

class RozetWidget(tk.Frame):
    def __init__(self,pencere):
        super().__init__(pencere)

        self.baslik= tk.Label(self, text="Kazanılan Rozetler", font=("Arial", 12, "bold"))
        self.baslik.pack(anchor="w", pady=(0,5))

        self.rozet_alani=tk.Frame(self)
        self.rozet_alani.pack(fill="x")

    def rozetleri_goster(self, rozet_listesi):
        #eski rozetleri ekrandan temizle
        for widget in self.rozet_alani.winfo_children():
            widget.destroy()
        if not rozet_listesi:
            bilgi=tk.Label(self.rozet_alani, text="Henüz hiç rozet kazanılmadı..", fg="gray", font=("Arial", 10, "italic"))
            bilgi.pack(anchor="w")
            return
        for rozet_adi in rozet_listesi:
            rozet_etiketi = tk.Label(self.rozet_alani,
                                     text=f"{rozet_adi}",
                                     bg='#FFD700', fg="black",
                                     font=("Arial", 10, "bold"),
                                     padx=5, pady=2)
            rozet_etiketi.pack(side="left", padx=5)
            

