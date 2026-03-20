# Supabase URL ve Key bağlantısı
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def get_supabase() -> Client:
    """Merkezi Supabase bağlantısı."""
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("Supabase URL veya KEY bulunamadı! .env dosyasını kontrol edin.")
    return create_client(SUPABASE_URL, SUPABASE_KEY)

# Uygulama genelinde kullanılacak hazır istemci
supabase = get_supabase()