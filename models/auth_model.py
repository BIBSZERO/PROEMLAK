from dataclasses import dataclass
from typing import Optional
from enum import IntEnum

class UserLevel(IntEnum):
    UYE = 0          # Standart Üye (Senin istediğin başlangıç seviyesi)
    DANISMAN = 2     # Emlak Danışmanı
    ADMIN = 3        # Sen (Her yetkiye sahip)

@dataclass
class UserProfile:
    """
    Supabase 'profiles' tablosundaki bir satırın 
    Python tarafındaki temiz karşılığı.
    """
    id: str
    full_name: str
    email: str
    telefon: str
    user_level: UserLevel = UserLevel.UYE
    created_at: Optional[str] = None

    @staticmethod
    def from_dict(data: dict):
        """
        Supabase'den gelen sözlük (dict) verisini 
        UserProfile nesnesine dönüştürür.
        """
        return UserProfile(
            id=str(data.get("id", "")), # Eğer None gelirse "" (boş metin) yap ve str'ye çevir
            full_name=str(data.get("full_name", "İsimsiz Kullanıcı")),
            email=str(data.get("email", "")),
            telefon=str(data.get("telefon", "")),
            user_level=UserLevel(data.get("user_level", 0)),
            created_at=data.get("created_at")
        )

    def to_dict(self):
        """
        Gerektiğinde nesneyi tekrar sözlüğe çevirir.
        """
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "telefon": self.telefon,
            "user_level": self.user_level
        }