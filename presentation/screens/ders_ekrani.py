import tkinter as tk
from bll.code_runner import CodeRunner

class DersEkrani(tk.Frame):
    def __init__(self, parent, ana_menuye_don_komutu,ders_tamamlandi_komutu):
        super().__init__(parent)
        
        self.code_runner = CodeRunner()
        self.ana_menuye_don_komutu = ana_menuye_don_komutu
        self.aktif_ders = None # Hangi dersi çözdüğümüzü burada tutsun diye yazdım
        self.ders_tamamlandi_komutu=ders_tamamlandi_komutu

        self.ust_panel = tk.Frame(self)
        self.ust_panel.pack(fill="x", pady=10, padx=20)

        self.btn_geri = tk.Button(self.ust_panel, text="⬅ Ana Menüye Dön", command=self.ana_menuye_don_komutu)
        self.btn_geri.pack(side="left")

        self.lbl_soru = tk.Label(self.ust_panel, text="Görev: ...", font=("Arial", 12, "bold"))
        self.lbl_soru.pack(side="left", padx=20)

        # kodlama alanım
        self.txt_kod = tk.Text(self, height=10, width=50, font=("Courier", 12), bg="#2b2b2b", fg="#ffffff", insertbackground="white")
        self.txt_kod.pack(pady=5, padx=20, fill="x")

        # çalıştırma butonum
        self.btn_calistir = tk.Button(self, text="Kodu Çalıştır! ", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), command=self.kodu_calistir)
        self.btn_calistir.pack(pady=10)

        #terminal alanı
        self.lbl_cikti_baslik = tk.Label(self, text="Terminal Çıktısı:", font=("Arial", 10, "bold"))
        self.lbl_cikti_baslik.pack(anchor="w", padx=20)

        self.txt_cikti = tk.Text(self, height=5, width=50, font=("Courier", 11), bg="black", fg="#00FF00", state="disabled")
        self.txt_cikti.pack(pady=5, padx=20, fill="x")

    def aktif_dersi_ayarla(self, ders):
        """Main.py'den çağrılıp bu ekrana hangi dersin verisini işleyeceğini söyler."""
        self.aktif_ders = ders
        self.lbl_soru.config(text=f"Görev: {ders.ders_basligi} konusunu tamamlayın.")
        
        # Ekran her açıldığında eski kodları ve çıktıları temizlesin diye yazdım
        self.txt_kod.delete("1.0", tk.END)
        self.txt_cikti.config(state="normal")
        self.txt_cikti.delete("1.0", tk.END)
        self.txt_cikti.config(state="disabled")

    def kodu_calistir(self):
        yazilan_kod = self.txt_kod.get("1.0", tk.END)
        
        # BLL CodeRunner üzerinden kodu derlesin ve sonucu alsın diye yadım 
        sonuc = self.code_runner.kod_calistir(yazilan_kod)
        
        # Terminal ekranına yazdıralım
        self.txt_cikti.config(state="normal")
        self.txt_cikti.delete("1.0", tk.END)
        self.txt_cikti.insert(tk.END, sonuc)
        
        if self.aktif_ders and self.aktif_ders.dogru_cevap:
            beklenen_cevap = str(self.aktif_ders.dogru_cevap).strip().lower()
            gercek_sonuc = sonuc.strip().lower()
            
            if beklenen_cevap == gercek_sonuc:
                self.txt_cikti.insert(tk.END, "\nTEBRİKLER! Görevi başarıyla tamamladınız!")
                #eğer fonksiyon geçildiyse parametre olarak, main.py ye gitsin ve ders verisini göndersin istediğimden yazdım
                if self.ders_tamamlandi_komutu:
                    self.ders_tamamlandi_komutu(self.aktif_ders)
            else:
                self.txt_cikti.insert(tk.END, "\nÇıktı beklenen cevapla eşleşmiyor. Tekrar deneyin.")
                
        self.txt_cikti.config(state="disabled")