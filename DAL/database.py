class DatabaseManager:
    """
    Singleton SQLAlchemy motor ve oturum yöneticisi. 
    Uygulama boyunca tek bir engine örneği yaşar. 
    """
    _instance: "DatabaseManager | None" = None