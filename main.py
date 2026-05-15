import tkinter as tk
from presentation.screens.ders_ekrani import DersEkrani
def main():
    root = tk.Tk()
    root.title("YazılımGo - Kod Editörü")
    root.geometry("500x450")

    print("KOd editörü testi: ")
    ders_ekrani=DersEkrani(root)
    ders_ekrani.pack(fill="both", expand=True)

    root.mainloop()

if __name__ == "__main__":
    main()