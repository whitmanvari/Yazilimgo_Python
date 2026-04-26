#Config.py aslında c#taki appsetting.json dosyasına benzer bir yapıdadır.
#Bu dosyada uygulamanın genel yapılandırma ayarları tutulur.
import os #--> os aslında c#taki System.IO sınıfına benzer bir yapıdır. Dosya ve klasör yollarını yönetmek için kullanılır.

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_YOLU  = os.path.join(BASE_DIR, "db", "yazilimgo.db")
