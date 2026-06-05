import tkinter as tk
from bll.code_runner import CodeRunner
from tkinter import ttk
import time
import threading
#tkinter thread safe değil. Tkinter "single-threaded" çalışır.

class DersEkrani(tk.Frame):
    def __init__(self, parent, ana_menuye_don_komutu, ders_tamamlandi_komutu):
        super().__init__(parent, bg="#f0f0f0")
        
        self.code_runner = CodeRunner()
        self.ana_menuye_don_komutu = ana_menuye_don_komutu
        self.ders_tamamlandi_komutu = ders_tamamlandi_komutu
        self.aktif_ders = None

        self.header_frame = tk.Frame(self, bg="#ffffff", pady=10)
        self.header_frame.pack(fill="x", side="top")
        
        self.btn_geri = tk.Button(self.header_frame, text="⬅ Ana Menüye Dön", command=self.ana_menuye_don_komutu)
        self.btn_geri.pack(side="left", padx=20)
        self.lbl_soru = tk.Label(self.header_frame, 
                         text="Görev: ...", 
                         font=("DejaVu Sans", 12, "bold"), 
                         bg="#ffffff", 
                         wraplength=700,  
                         justify="center")
        self.lbl_soru.pack(side="left", padx=30,pady=15)
        

        self.content_frame = tk.Frame(self, bg="#f0f0f0")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.txt_kod = tk.Text(self.content_frame, height=10, font=("DejaVu Sans", 12), bg="#2b2b2b", fg="#ffffff", insertbackground="white")
        self.txt_kod.pack(fill="x", pady=5)

        self.lbl_cikti_baslik = tk.Label(self.content_frame, text="Terminal Çıktısı:", bg="#f0f0f0", font=("DejaVu Sans", 14, "bold"))
        self.lbl_cikti_baslik.pack(anchor="w", pady=(10, 0))
        
        self.txt_cikti = tk.Text(self.content_frame, height=5, font=("DejaVu Sans", 11), bg="black", fg="#FAA2A2", state="disabled")
        self.txt_cikti.pack(fill="x", pady=5)

        self.footer_frame = tk.Frame(self, bg="#f0f0f0")
        self.footer_frame.pack(fill="x", side="bottom", padx=20, pady=20)

        self.progress_frame = tk.Frame(self.footer_frame, bg="#f0f0f0")
        self.progress_frame.pack(fill="x")

        self.progress = ttk.Progressbar(self.progress_frame, mode="indeterminate", length=200)
        self.progress.pack(fill="x", pady=5)
        self.progress.pack_forget() # Başta gizli

        self.lbl_status = tk.Label(self.progress_frame, text="Kod inceleniyor...", bg="#f0f0f0")
        self.lbl_status.pack_forget()

        self.btn_calistir = tk.Button(self.footer_frame, text="Kodu Çalıştır!", bg="#FAA2A2", fg="white", font=("DejaVu Sans", 10, "bold"), command=self.kodu_calistir)
        self.btn_calistir.pack(pady=10)

        self.lbl_mesaj = tk.Label(self.footer_frame, text="", font=("DejaVu Sans", 14, "bold"), bg="#f0f0f0")
        self.lbl_mesaj.pack()

        # ProgressBar Stili
        style = ttk.Style()
        style.theme_use('default')
        style.configure("my.Horizontal.TProgressbar", thickness=10, background='#FAA2A2', troughcolor="#e0e0e0")
        self.progress.configure(style="my.Horizontal.TProgressbar")

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
            self.lbl_mesaj.config(text="Tebrikler! Doğru cevap. ", fg="#FDB9B9")
            self.ders_tamamlandi_komutu(self.aktif_ders)
        else:
            self.lbl_mesaj.config(text="Tekrar dene, cevap yanlış..", fg="red")