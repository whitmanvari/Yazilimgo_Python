import sqlite3
import hashlib

class Database:
    def __init__(self):
        self.baglanti = sqlite3.connect("DB/yazilimgo.db")
        self.imlec = self.baglanti.cursor()

        self.imlec.execute("PRAGMA foreign_keys = ON")
        self.tablolari_olustur()

    def tablolari_olustur(self):
        #Kullanıcı tablosu 
        self.imlec.execute("""
            CREATE TABLE IF NOT EXISTS Kullanicilar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kullanici_adi TEXT NOT NULL UNIQUE,
                sifre TEXT NOT NULL,
                rol TEXT NOT NULL,
                toplam_xp INTEGER DEFAULT 0,
                seviye INTEGER DEFAULT 1
            )
        """)
 
        #Kategoriler tablosu
        self.imlec.execute("""
            CREATE TABLE IF NOT EXISTS Kategoriler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kategori_adi TEXT NOT NULL UNIQUE,
                aciklama TEXT
            )
        """)

        #Sorular tablosu
        self.imlec.execute("""
            CREATE TABLE IF NOT EXISTS Sorular (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                soru_metni TEXT NOT NULL,
                dogru_cevap TEXT NOT NULL,
                kategori_id INTEGER NOT NULL,
                FOREIGN KEY (kategori_id) REFERENCES Kategoriler(id) ON DELETE CASCADE,
                XP_degeri INTEGER DEFAULT 10,
                siklar TEXT NOT NULL                              
            )""")
        
        #Çözümler tablosu (Numpy/ Mathplotlib analizleri için)
        self.imlec.execute("""
            CREATE TABLE IF NOT EXISTS Cozumler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                soru_id INTEGER NOT NULL,
                kullanici_id INTEGER NOT NULL,
                cozum TEXT NOT NULL,
                verilen_cevap TEXT NOT NULL,
                dogru_mu BOOLEAN NOT NULL,
                cozum_tarihi DATE DEFAULT CURRENT_DATE,
                FOREIGN KEY (soru_id) REFERENCES Sorular(id) ON DELETE CASCADE,
                FOREIGN KEY (kullanici_id) REFERENCES Kullanicilar(id) ON DELETE CASCADE
            )
        """)

        
        self.baglanti.commit()
        print("Bilgi Mesajı: Veritabanı başarı ile kuruldu!")