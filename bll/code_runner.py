import io
from contextlib import redirect_stdout

class CodeRunner:
    def kod_calistir(self, kullanici_kodu: str) ->str:
        #geçici bir metin alanı açar
        yakalanan_cikti=io.StringIO()

        try:
            #kodları terminale değil de yakalanan_ciktiya yazdır 
            with redirect_stdout(yakalanan_cikti):
                #python kodu gibi derler o boş sözlük 
                # ise güvenlik duvarı, kullanıcının yazdığı 
                # kodlar benim ana uygulamamın değişkenine 
                # veya hafızasına sızmasın diye koruma 
                exec(kullanici_kodu, {})
            sonuc=yakalanan_cikti.getvalue()
            #strip() trim() gibi çalışır 
            return sonuc.strip()
        except Exception as e:
            return f"Hata: {str(e)}"