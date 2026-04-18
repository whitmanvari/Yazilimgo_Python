import sqlite3
import hashlib
import json

class Database:
    def __init__(self):
        self.db_yolu = "DB/yazilimgo.db"
        self.baglanti_olustur()
        self.tablolari.olustur()
    
    def baglanti_olustur(self):
        self.baglanti=sqlite3.connect(self.db_yolu)
        self.imlec=self.baglanti.cursor()
        self.imlec.execute("PRAGMA foreign_keys = ON")

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
                cozum_aciklamasi TEXT,
                xp_degeri INTEGER DEFAULT 10,
                siklar_json TEXT NOT NULL,
                FOREIGN KEY (kategori_id) REFERENCES Kategoriler(id) ON DELETE CASCADE                              
            )""")
        
        #Çözümler tablosu (Numpy/ Mathplotlib analizleri için)
        self.imlec.execute("""
            CREATE TABLE IF NOT EXISTS Cozumler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                soru_id INTEGER NOT NULL,
                kullanici_id INTEGER NOT NULL,
                verilen_cevap TEXT NOT NULL,
                dogru_mu BOOLEAN NOT NULL,
                cozum_tarihi DATE DEFAULT CURRENT_DATE,
                FOREIGN KEY (soru_id) REFERENCES Sorular(id) ON DELETE CASCADE,
                FOREIGN KEY (kullanici_id) REFERENCES Kullanicilar(id) ON DELETE CASCADE
            )
        """)

        
        self.baglanti.commit()
        print("Bilgi Mesajı: Veritabanı başarı ile kuruldu!")

        def _sifre_hashle(self, ham_sifre: str) -> str:
            """Verilen ham şifreyi SHA-256 algoritmasıyla hashler."""
            return hashlib.sha256(ham_sifre.encode('utf-8')).hexdigest()
        
        def kullanici_ekle(self, kullanici_adi: str, sifre: str, rol: str) -> bool:
            try:
                guvenli_sifre = self._sifre_hashle(sifre)
                self.imlec.execute("""INSERT INTO Kullanicilar (kullanici_adi, sifre, rol) VALUES (?, ?, ?)""",
                                    (kullanici_adi, guvenli_sifre, rol))
                self.baglanti.commit()
                return True
            except sqlite3.IntegrityError:
                print("Hata: Bu kullanıcı adı zaten kullanılıyor.")
                return False
            except Exception as e:
                print(f"Hata: {e}")
                return False
        
        def kullanici_getir(self, kullanici_adi: str, sifre: str) -> tuple:
            guvenli_sifre = self._sifre_hashle(sifre)
            self.imlec.execute("""SELECT * FROM Kullanicilar WHERE kullanici_adi = ? AND sifre = ?""",
                                (kullanici_adi, guvenli_sifre))
            return self.imlec.fetchone()
        
        def kategori_ekle(self, kategori_adi: str, aciklama: str = "") -> bool:
            try:
                self.imlec.execute("""INSERT INTO Kategoriler (kategori_adi, aciklama) VALUES (?, ?)""",
                                    (kategori_adi, aciklama))
                self.baglanti.commit()
                return True
            except sqlite3.IntegrityError:
                print("Hata: Bu kategori adı zaten kullanılıyor.")
                return False
            except Exception as e:
                print(f"Hata: {e}")
                return False
            
        def soru_ekle(self, soru_metni: str, dogru_cevap: str, kategori_id: int, cozum_aciklamasi: str, siklar: list, xp_degeri: int = 10) -> bool:
            try:
                siklar_json = json.dumps(siklar, ensure_ascii=False)
                self.imlec.execute("""INSERT INTO Sorular (soru_metni, dogru_cevap, kategori_id, cozum_aciklamasi, xp_degeri, siklar_json) VALUES (?, ?, ?, ?, ?, ?)""",
                                    (soru_metni, dogru_cevap, kategori_id, cozum_aciklamasi, xp_degeri, siklar_json))
                self.baglanti.commit()
                return True
            except Exception as e:
                print(f"Hata: {e}")
                return False
            
    
