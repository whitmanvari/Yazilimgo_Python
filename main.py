import tkinter as tk
from presentation.components.xp_bar import XPBar

def main():
    # Ana pencereyi oluştur
    root = tk.Tk()
    root.title("YazılımGo - Tkinter UI Test")
    root.geometry("400x200")

    # Kendi yazdığımız özel XPBar kutusunu ana pencereye ekliyoruz
    xp_bileseni = XPBar(root)
    xp_bileseni.pack(pady=50, padx=20, fill="x")

    # BLL'den Ahmett'in verilerinin geldiğini varsayalım
    xp_bileseni.guncelle(mevcut_xp=345, seviye=4)

    # Pencereyi açık tut
    root.mainloop()

if __name__ == "__main__":
    main()