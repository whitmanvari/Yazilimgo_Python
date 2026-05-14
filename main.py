import tkinter as tk
from presentation.components.xp_bar import XPBar
from presentation.components.rozet_widget import RozetWidget

def main():
    root = tk.Tk()
    root.title("YazılımGo - Öğrenci Paneli Test")
    root.geometry("450x300")

    print("ui testi")

    xp_bileseni = XPBar(root)
    xp_bileseni.pack(pady=20, padx=20, fill="x")
    xp_bileseni.guncelle(mevcut_xp=345, seviye=4)

    rozet_bileseni = RozetWidget(root)
    rozet_bileseni.pack(pady=10, padx=20, fill="x")

    # BLL'den rozet verilerinin geldiğini varsayalım
    kazanilan_rozetler = ["İlk Adım", "Alev Bekçisi", "Hatasız Kod"]
    rozet_bileseni.rozetleri_goster(kazanilan_rozetler)

    root.mainloop()

if __name__ == "__main__":
    main()