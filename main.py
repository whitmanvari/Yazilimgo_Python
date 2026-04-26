from dal.database import DatabaseManager

# 1. Veritabanı motorunu başlat ve tabloları oluştur
db = DatabaseManager()
db.init_db()
print("Tablolar başarıyla oluşturuldu.")

# 2. Singleton kontrolü (Aynı RAM adresini mi kullanıyorlar?)
db2 = DatabaseManager()
assert db is db2, "Singleton çalışmıyor!"
print("Singleton doğrulandı.")