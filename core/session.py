from models.auth_model import UserProfile, UserLevel

class Sessions:
    def __init__(self):
        self.user = None           # Supabase'den gelen ham ham kullanıcı (auth.user)
        self.user_profile = None   # Bizim oluşturduğumuz UserProfile model nesnesi
        self.is_logged_in = False

    def set_session(self, user_data, profile_data: dict):
        """Kullanıcı giriş yaptığında bilgileri hafızaya alır."""
        self.user = user_data
        # Sözlük verisini UserProfile modeline dönüştürüp saklıyoruz
        self.user_profile = UserProfile.from_dict(profile_data)
        self.is_logged_in = True

    def clear(self):
        """Çıkış yapıldığında hafızayı sıfırlar."""
        self.user = None
        self.user_profile = None
        self.is_logged_in = False

    # --- Yetki Kontrolleri (@property kullanımı) ---

    @property
    def current_level(self) -> int:
        """Kullanıcının sayısal seviyesini döndürür. Giriş yoksa -1."""
        return self.user_profile.user_level if self.user_profile else -1

    @property
    def is_uye(self) -> bool:
        """Sadece Level 0 mı?"""
        return self.current_level == UserLevel.UYE

    @property
    def is_danisman(self) -> bool:
        """En az Danışman seviyesinde mi? (Danışman veya Admin)"""
        return self.current_level >= UserLevel.DANISMAN

    @property
    def is_admin(self) -> bool:
        """Tam yetkili Admin mi?"""
        return self.current_level == UserLevel.ADMIN

# Her yerden erişilecek tekil oturum nesnesi
current_session = Sessions()