# Yazilimgo_Python: Oyunlaştırılmış Kodlama Eğitmeni
İleri Programlama dersi için, programlama öğrenme sürecini oyunlaştırılmış interaktif testler, performans analizleri ve görsel öğrenme eğrileri ile destekleyen bir masaüstü eğitim platformudur. Öğretim tasarımı ilkelerine uygun düzenlenmiştir. 

## 🏗 Mimari Deseni (Architectural Pattern)
Proje, modülerlik ve sürdürülebilirlik için **N-Tier (Katmanlı Mimari)** yapısını kullanır:
* **Presentation (Tkinter & Matplotlib):** Kullanıcı dostu arayüz ve analiz grafiklerini sunar.
* **Business (BLL):** Soru mantığı, XP/Level hesaplamaları ve **NumPy** tabanlı başarı analizlerini yönetir.
* **DAL (Data Access):** SQLite üzerinden veritabanı işlemlerini koordine eder.
* **Core:** Tüm katmanlar için merkezi doğrulama (Validation) sağlar.

* ## 🛠 Kullanılan Teknolojiler & Tasarım Desenleri
* **NumPy:** Öğrenci hata oranları ve gelişim verilerinin matris tabanlı matematiksel analizi.
* **Matplotlib:** Öğrenme eğrilerinin ve başarı istatistiklerinin görselleştirilmesi.
* **SQLite:** Veri kalıcılığı ve ilişkisel veritabanı yönetimi.
* **Singleton Pattern:** Veritabanı bağlantısında tekil nesne yönetimi.
* **Strategy Pattern:** Farklı zorluk seviyelerine göre puan hesaplama algoritmaları.

```markdown
## 🗺️ Veritabanı Mimarisi (ER Şeması)
```mermaid
erDiagram
    KULLANICILAR ||--o{ ILERLEME_DURUMU : "çözer"
    KULLANICILAR ||--o{ KULLANICI_KAZANIMLARI : "kazanır"
    DERS_MODULLERI ||--o{ DERSLER : "içerir"
    DERS_MODULLERI |o--o{ DERS_MODULLERI : "ön koşul (Self-Ref)"
    DERSLER ||--o{ ILERLEME_DURUMU : "çözülür"
    KAZANIM_TANIMI ||--o{ KULLANICI_KAZANIMLARI : "verilir"

    KULLANICILAR {
        int kullanici_id PK "Otomatik Artan"
        string kullanici_adi UK "Benzersiz"
        string email UK "Benzersiz"
        string parola_hash "SHA-256 Şifreli"
        int toplam_xp 
        int seviye 
        int gunluk_hedef_xp 
        int gun_serisi 
        date son_aktif_tarihi 
        datetime kayit_tarihi 
    }

    DERS_MODULLERI {
        int modul_id PK
        int zorunlu_onceki FK "Özyinelemeli İlişki"
        string modul_adi 
        string dil 
        int sira_no 
        float xp_carpani "Oyunlaştırma Çarpanı"
    }

    DERSLER {
        int ders_id PK
        int modul_id FK "Modüle Bağlı"
        string ders_basligi 
        string ders_turu 
        string soru_metni 
        string kod_sablonu 
        string dogru_cevap 
        int kazanilan_xp 
        int sira_no 
    }

    ILERLEME_DURUMU {
        int ilerleme_id PK
        int kullanici_id FK "Kavşak Bağlantısı 1"
        int ders_id FK "Kavşak Bağlantısı 2"
        string durum "Check Constraint"
        int deneme_sayisi 
        int kazanilan_xp 
        datetime tamamlanma_tarihi 
        int sure_saniye 
    }

    KAZANIM_TANIMI {
        int kazanim_id PK
        string kazanim_adi 
        string ikon_adi 
        string kosul_turu "Check Constraint"
        int kosul_degeri 
    }

    KULLANICI_KAZANIMLARI {
        int id PK
        int kullanici_id FK "Kavşak Bağlantısı 1"
        int kazanim_id FK "Kavşak Bağlantısı 2"
        datetime kazanilma_tarih 
    }

```