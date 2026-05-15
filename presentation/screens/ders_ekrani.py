import tkinter as tk
from bll.code_runner import CodeRunner

class DersEkrani(tk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        #bll code runner motorunu bağlamak için yazdım
        self.code_runner=CodeRunner()

        self.lbl_soru=tk.Label(self, text="Görev: Ekrana print() methodunu kullanarak 'Merhaba!' yazdırın", font=("Arial", 12, "bold"))
        self.lbl_soru.pack(pady=(10,5), anchor="w", padx=20)

        self.txt_kod=tk.Text(self, height=10, width=50, font=("Courier", 12),bg='#2b2b2b', fg='#ffffff', insertbackground='white' )
        self.txt_kod.pack(pady=5, padx=20, fill="x")

        self.btn_calistir=tk.Button(self, text="Kodu Çalıştır", bg='#4CAF50', fg='white', font=("Arial", 10, "bold"), command=self.kodu_calistir)
        self.btn_calistir.pack(pady=10)

        self.lbl_cikti_baslik=tk.Label(self, text="Terminal Çıktısı: ", font=("Arial", 10,"bold"))
        self.lbl_cikti_baslik.pack(anchor="w", padx=20)

        self.txt_cikti=tk.Text(self, height=5, width=50, font=("Courier", 11), bg='black', fg='#00FF00', state="disabled")
        self.txt_cikti.pack(pady=5,padx=20, fill="x")

    def kodu_calistir(self):
        #metni editörden aldım
        yazilan_kod=self.txt_kod.get("1.0", tk.END)

        sonuc=self.code_runner.kod_calistir(yazilan_kod)

        self.txt_cikti.config(state="normal")
        self.txt_cikti.delete("1.0", tk.END)
        self.txt_cikti.insert(tk.END, sonuc)
        self.txt_cikti.config(state="disabled")


