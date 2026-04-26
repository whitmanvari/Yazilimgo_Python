from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from config import DB_YOLU

from Yazilimgo_Python.entities.base import Base 
# C#'taki DbSet<> tanımlamalarının karşılığı budur, kullanmasak bile import etmeliyiz ki SQLAlchemy tabloların varlığından haberdar olsun.
from Yazilimgo_Python.entities.kullanici import Kullanici
from Yazilimgo_Python.entities.modul import DersModulu
from Yazilimgo_Python.entities.ders import Ders
from Yazilimgo_Python.entities.ilerleme import IlerlemeKaydi
from Yazilimgo_Python.entities.kazanim import KazanimTanimi, KullaniciKazanim
# Not: Kullandığım editör visual studio code bunları kullanılmayan değişken olarak görse de, yine de SQLAlchemy okuyacaktır. 


class DatabaseManager:
    """
    Bilgilendirme (Docstring):
    Singleton SQLAlchemy motor ve oturum yöneticisi. 
    Uygulama boyunca tek bir engine örneği yaşar. 

    """
    #instance class gibi stack'te tutulmaz, örneklemi alınarak artık heap'te tutulan bir obje haline gelir. 
    #c#taki new'lenmiş bir sınıfın örneği gibi düşünülebilir. 
    #Encapsulation kullanılmış 'private' keywordü yerine _ kullanılmıştır Python'da. Bu encapsulation sayesinde dışarıdan erişim engellenmiş olur. (Override etmeleri dış sınıfların engellenmiş olur.)
    _instance: "DatabaseManager | None" = None

    #Engine--> SQLAlchemy'nin fiziksel bağlantı merkezini tutar. Python kodlarını veritabanı sorhularına (raw sql) çevirir. ADO.NET karşılığı sqlcConnection ve arkaplandaki ConnectionString ayarlarının birleşimidir.
    _engine = None

    #SessionLocal--> SQLAlchemy'nin oturum yönetimini sağlar. Veritabanı işlemlerini yönetir. Unit of Work (İş Birimi) tasarım desenini uygular. Veritabanı işlemlerini tek bir oturumda yönetir. C#'taki DbContext'e benzer şekilde düşünülebilir.
    #Biz her veri eklemek istediğimizde yeni bir Session (Oturum) isteriz. _engine uygulamanın tamamı için tektir (Global) ama Session bize özeldir (Local).
    _SessionLocal = None

    """
    Bilgilendirme (Docstring):
    c# karşılığı:
    using (var context = new MyDbContext()) 
{
    var hazal = new Kullanici { Adi = "Hazal" };
    context.Kullanicilar.Add(hazal); 
    context.SaveChanges();           // Veritabanına yolla
}

    Python'da ise:
    with DatabaseManager().get_session() as session:
    hazal = Kullanici(kullanici_adi="Hazal")
    session.add(hazal)  
    session.commit()    # Veritabanına yolla
    """

    #new methodu: new methodu sınıfın örneği oluşturulurken çağrılır. 
    # Singleton tasarım deseninde, sınıfın tek bir örneğinin oluşturulmasını sağlamak için kullanılır. 
    # Eğer _instance None ise, yeni bir örnek oluşturulur ve _instance'a atanır. 
    # Sonraki çağrılarda, zaten var olan örnek döndürülür. Böylece uygulama boyunca tek bir DatabaseManager örneği yaşar.
    def __new__(cls) -> "DatabaseManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._engine = create_engine(
                f"sqlite:///{DB_YOLU}",
                echo=False,          
                connect_args={"check_same_thread": False},
            )
            cls._instance._SessionLocal = sessionmaker(
                bind=cls._instance._engine,
                autocommit=False,
                autoflush=False,
            )
        return cls._instance
    
    #init_db methodu: Bu method, SQLAlchemy'nin Base.metadata.create_all() fonksiyonunu kullanarak tüm tabloları oluşturur. 
    #Çalıştığı anda from importla çağırdığımız tüm o entityleri okur.
    #c#karşılığı ise package manager console'a yazdığımız "Update-Database" komutudur.
    def init_db(self) -> None:
        """Tüm tabloları oluşturur. main.py'de bir kez çağrılır."""
        Base.metadata.create_all(bind=self._engine)

    def get_session(self) -> Session:
        """Repository'lerin kullanacağı oturum nesnesi döndürür."""
        return self._SessionLocal()




"""Bilgilendirme (Docstring):
UNIT OF WORK (İŞ BİRİMİ) TASARIM DESENİ:
Unit of Work, uygulamanın veritabanına yapacağı birden fazla ekleme, silme veya güncelleme işlemini tek bir liste 
halinde RAM'de tutan ve bu listenin tamamını tek seferde (tek bir transaction içinde) veritabanına gönderen bir tasarım desenidir.
NEDEN KULLANIRIZ?
Veri Bütünlüğü (Rollback): Diyelim ki aynı anda 1 Kullanıcı eklediK, 
1 İlerleme eklediK ve 1 Kazanım eklediK. Bunlar veritabanına giderken 3. işlemde hata çıkarsa, UoW ilk 2 işlemi de geri alır (Rollback).
Veritabanında yarım kalmış bozuk veri oluşmasını engeller. Ya hepsi kaydolur ya hiçbiri.
Performans (Ağ Trafiği): Veritabanına her kayıt eklendiğinde 
ağı meşgul edip yeni bir bağlantı açmak yerine, tüm işlemleri bellekte biriktirir 
ve tek bir SQL bloğu halinde veritabanına yollar. Ağ trafiğini minimize eder.

Örneğin c#'ta Entity Framework Core --> DbContext sınıfının kendisi doğrudan Unit of Work desenini uygular. 
Python'da ise SQLAlchemy'nin Session sınıfı Unit of Work desenini uygular.
Yani c#'ta savechanges() methoduna kadar veritabanına hiçbir değişiklik gitmez, python'da ise commit() methoduna kadar hiçbir değişiklik gitmez.

UoW Kayıtları RAM'e Alma İşlemi: C#'ta .Add() / Python'da .add()

UoW Transaction'ı Çalıştırma İşlemi: C#'ta .SaveChanges() / Python'da .commit()

"""