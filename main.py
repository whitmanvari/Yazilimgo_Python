from bll.code_runner import CodeRunner

def main():
    runner = CodeRunner()

    print("\n--- CODE RUNNER TESTİ ---")

    basit_kod = """
isim = "Hazal"
print("Merhaba " + isim)
"""
    print("1: Basit Değişken ve Print]")
    sonuc1 = runner.kod_calistir(basit_kod)
    print(f"Çıktı: {sonuc1}")

    matematik_kodu = """
sayi1 = 15
sayi2 = 30
toplam = sayi1 + sayi2
if toplam > 40:
    print("Geçti")
else:
    print("Kaldı")
"""
    print("2: If-Else ve Matematiksel İşlem]")
    sonuc2 = runner.kod_calistir(matematik_kodu)
    print(f"Çıktı: {sonuc2}")

    hatali_kod = """
print(tanimlanmamis_degisken)
"""
    print("3: Hatalı Kod Yakalama]")
    sonuc3 = runner.kod_calistir(hatali_kod)
    print(f"Çıktı: {sonuc3}")

if __name__ == "__main__":
    main()