from sqlalchemy.orm import DeclarativeBase
#declarative base--> base(zemin) adında yeni bir sınıf yarattım, sqlachemy'nin sunduğu bir şablon bu. classları sql tablolarına çevirmeyi sağlıyor.
#base sınıfını declarative base türünde hazırlıyorum. pass ile hatasız bir şekilde geçsin diye yazıyorum. 
class Base(DeclarativeBase):
    pass  

#diğer tüm varlıklarımı ben base'den türeteceğim bu sayede sql tablolarım açığa çıkacak. 
#bu yönteme sqlalchemy'de declarative mapping(bildirimsel eşleşme) deseni deniyor. Merkezi bir kayıt defteri (registry) oluşturmuş oluyorum. 
#Bu esnek yapı ile solid prensiplerine uygun bir işlem yapmış oluyorum. 