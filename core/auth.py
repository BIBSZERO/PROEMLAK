# Giriş yapma, Kayıt olma, Çıkış işlemleri
from core.config import db
from core.session import current_session
from models.auth_model import UserLevel

class AuthGuard:
    @staticmethod
    def initialize_session():
        """
        Uygulama ilk açıldığında çalışır. 
        Supabase'de aktif bir oturum (token) varsa kullanıcıyı hatırlar.
        """
        try:
            # 1. Supabase'den mevcut oturumu sorgula
            session = db.auth.get_session()
            
            if session and session.user:
                # 2. Eğer oturum varsa, profiles tablosundan yetki ve detayları çek
                res = db.table("profiles").select("*").eq("id", session.user.id).single().execute()
                
                if res.data:
                    # 3. Hafızayı (Session) otomatik doldur
                    current_session.set_session(session.user, res.data)
                    return True
            return False
        except Exception:
            # Oturum yoksa veya hata oluşursa sessizce False dön
            return False

    @staticmethod
    def is_authorized(required_level: UserLevel = UserLevel.UYE) -> bool:
        """
        Belirli bir sayfaya giriş yetkisi var mı kontrol eder.
        Örn: AuthGuard.is_authorized(UserLevel.ADMIN)
        """
        if not current_session.is_logged_in:
            return False
        
        return current_session.current_level >= required_level

    @staticmethod
    def get_current_user_id():
        """O anki kullanıcının ID'sini güvenli bir şekilde döndürür."""
        return current_session.user.id if current_session.user else None