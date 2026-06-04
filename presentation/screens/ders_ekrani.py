import tkinter as tk
from bll.code_runner import CodeRunner
from tkinter import ttk
import time
import threading
#tkinter thread safe değil. Tkinter "single-threaded" çalışır.

class DersEkrani(tk.Frame):
    def __init__(self, parent, ana_menuye_don_komutu,ders_tamamlandi_komutu):
        super().__init__(parent)
        
        self.code_runner = CodeRunner()
        self.progress_frame= tk.Frame(self, bg="#f0f0f0")
        self.progress_frame.pack(fill="x", pady=5)

        self.progress = ttk.Progressbar(self.progress_frame, mode="indeterminate", length=200)
        self.ana_menuye_don_komutu = ana_menuye_don_komutu
        self.aktif_ders = None # Hangi dersi çözdüğümüzü burada tutsun diye yazdım
        self.ders_tamamlandi_komutu=ders_tamamlandi_komutu
        style=ttk.Style()
        style.theme_use('default')
        style.configure("my.Horizontal.TProgressbar",
                        thickness=10,
                        troughcolor="#e0e0e0",
                        background="#4CAF50")
        
        self.progress.configure(style="my.Horizontal.TProgressbar")

        self.ust_panel = tk.Frame(self)
        self.ust_panel.pack(fill="x", pady=10, padx=20)

        self.btn_geri = tk.Button(self.ust_panel, text="⬅ Ana Menüye Dön", command=self.ana_menuye_don_komutu)
        self.btn_geri.pack(side="left")

        self.lbl_soru = tk.Label(self.ust_panel, text="Görev: ...", font=("DejaVu Sans", 12, "bold"))
        self.lbl_soru.pack(side="left", padx=20)

        # kodlama alanım
        self.txt_kod = tk.Text(self, height=10, width=50, font=("DejaVu Sans", 12), bg="#2b2b2b", fg="#ffffff", insertbackground="white")
        self.txt_kod.pack(pady=5, padx=20, fill="x")

        self.lbl_status=tk.Label(self.progress_frame, text="Kod inceleniyor...", bg="#f0f0f0")
        self.lbl_status.pack_forget()

        # çalıştırma butonum
        self.btn_calistir = tk.Button(self, text="Kodu Çalıştır! ", bg="#4CAF50", fg="white", font=("DejaVu Sans", 10, "bold"), command=self.kodu_calistir)
        self.btn_calistir.pack(pady=10)

        self.lbl_mesaj=tk.Label(self, text="", font=("DejaVu Sans", 10, "bold"),bg="#ffffff")
        self.lbl_mesaj.pack(pady=5)

        #terminal alanı
        self.lbl_cikti_baslik = tk.Label(self, text="Terminal Çıktısı:", font=("DejaVu Sans", 10, "bold"))
        self.lbl_cikti_baslik.pack(anchor="w", padx=20)

        self.txt_cikti = tk.Text(self, height=5, width=50, font=("DejaVu Sans", 11), bg="black", fg="#00FF00", state="disabled")
        self.txt_cikti.pack(pady=5, padx=20, fill="x")

    def aktif_dersi_ayarla(self, ders):
        """Main.py'den çağrılıp bu ekrana hangi dersin verisini işleyeceğini söyler."""
        self.aktif_ders = ders
        self.lbl_mesaj.config(text="")
        self.lbl_soru.config(text=ders.soru_metni)
        
        # Ekran her açıldığında eski kodları ve çıktıları temizlesin diye yazdım
        self.txt_kod.delete("1.0", tk.END)
        self.txt_cikti.config(state="normal")
        self.txt_cikti.delete("1.0", tk.END)
        self.txt_cikti.config(state="disabled")

    def kodu_calistir(self):
        self.lbl_mesaj.config(text="")
        self.btn_calistir.config(state="disabled")
        self.lbl_status.pack()
        self.progress.pack(padx=20, fill="x") #görünür hale getirelim
        self.progress.start(10)
        
        
       
        #threading thread--> target kısmına arka planda ne yapacağını söyledik
        kod_thread = threading.Thread(target=self._arka_planda_calistir)
        kod_thread.start()

    def _arka_planda_calistir(self):
        print("Thread başladı...")
        time.sleep(3)
        #fonksiyon main threadinin dışında çalışıyor bu sayede burası donarsa arayüz donmaz hale geliyor
        kullanici_kodu = self.txt_kod.get("1.0", tk.END)
        sonuc=self.code_runner.kod_calistir(kullanici_kodu)
    #ms =0 diyoruz ki aftera, mainloopun bir sonraki iterasyonuna eklesin. İş ana thread kuyruğuna ekleniyor burada. 
        self.after(0,self._ekrani_guncelle, sonuc)

    def _ekrani_guncelle(self, sonuc):
        #burası main threadinde çalışıyor. 
        self.txt_cikti.config(state="normal")
        #1.satır o satırdaki 0. k
        # arakter (metin kutusunun en başına gitsin demek 1.0), tk.END ise sabit. metin kutusunun sonundaki gizli karakter (metin kutusunun sonuna git demek tk.END)
        self.txt_cikti.delete("1.0", tk.END)
        self.txt_cikti.insert("1.0", sonuc)
        self.txt_cikti.config(state="disabled")

        self.progress.stop()
        self.progress.pack_forget()
        self.lbl_status.pack_forget()
        self.btn_calistir.config(state="normal", text="Kodu Çalıştır...")
        if sonuc.strip() == self.aktif_ders.dogru_cevap.strip():
            self.lbl_mesaj.config(text="Tebrikler! Doğru cevap. ", fg="green")
            self.ders_tamamlandi_komutu(self.aktif_ders)
        else:
            self.lbl_mesaj.config(text="Tekrar dene, cevap yanlış..", fg="red")