# Kayıt, Giriş, Şifre Sıfırlama
from core.config import db
from core.session import current_session
from models.auth_model import UserProfile


class AuthService:
    @staticmethod
    def login(email: str, password: str):
        """Kullanıcı girişini yapar ve session'ı doldurur."""
        try:
            # 1. Supabase Auth ile giriş
            res = db.auth.sign_in_with_password({"email": email, "password": password})
            
            # HATA BURADAYDI: res.user_id yerine res.user.id kullanmalıyız
            if res.user:
                # 2. Profiles tablosundan detayları çek
                profile_res = db.table("profiles").select("*").eq("id", res.user.id).single().execute()
                
                # Mypy'ın beklediği dict tipini garanti ediyoruz
                if profile_res.data and isinstance(profile_res.data, dict):
                    current_session.set_session(res.user, profile_res.data)
                    return True, "Giriş başarılı!"
                
            return False, "Kullanıcı profil bilgileri bulunamadı."
        except Exception as e:
            return False, f"Giriş hatası: {str(e)}"
        
    @staticmethod
    def register(email: str, password: str, full_name: str, phone: str):
        """Yeni kullanıcı kaydeder ve profiles tablosuna Level 0 olarak işler."""
        try:
            # 1. Supabase Auth'a yeni kullanıcı ekle
            auth_res = db.auth.sign_up({"email": email, "password": password})

            if auth_res.user:
                # 2. Profiles tablosuna Level 0 (Üye) olarak detayları yaz
                db.table("profiles").insert({
                    "id": auth_res.user.id,
                    "full_name": full_name,
                    "email": email,
                    "telefon": phone,
                    "user_level": 0
                }).execute()
                return True, "Kayıt başarılı! Lütfen mailinizi onaylayın."
            return False, "Kayıt sırasında bir sorun oluştu."
        
        except Exception as e:
            return False, f"Hata: {str(e)}"
        
    @staticmethod
    def logout():
        """Oturumu hem Supabase'den hem de yerel hafızadan siler."""
        db.auth.sign_out()
        current_session.clear()
        return True