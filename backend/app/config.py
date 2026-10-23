"""Config loader — loads from .env (via python-dotenv)."""
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BASE_DIR / ".env"

if ENV_FILE.exists():
    load_dotenv(ENV_FILE)

def _env(key: str, default: str = "") -> str:
    return os.getenv(key, default)

def _env_int(key: str, default: int) -> int:
    val = os.getenv(key)
    return int(val) if val and str(val).isdigit() else default

# Database
DB_HOST = _env("DB_HOST", "127.0.0.1")
DB_PORT = _env_int("DB_PORT", 3306)
DB_USER = _env("DB_USER", "isp_billing")
DB_PASSWORD = _env("DB_PASSWORD", "")
DB_NAME = _env("DB_NAME", "isp_billing")

SQLALCHEMY_DATABASE_URI = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# FreeRADIUS
FREERADIUS_HOST = _env("FREERADIUS_HOST", "127.0.0.1")
FREERADIUS_SECRET = _env("FREERADIUS_SECRET", "")

# MikroTik
MIKROTIK_HOST = _env("MIKROTIK_HOST", "192.168.100.254")
MIKROTIK_PORT = _env_int("MIKROTIK_PORT", 1998)
MIKROTIK_USER = _env("MIKROTIK_USER", "hermes")
MIKROTIK_PASSWORD = _env("MIKROTIK_PASSWORD", "")

# Web
HOST = _env("HOST", "0.0.0.0")
PORT = _env_int("PORT", 793)
SECRET_KEY = _env("SECRET_KEY", "dev-only-secret")
JWT_SECRET = _env("JWT_SECRET", "dev-jwt-secret")

# Blockchain (optional)
BLOCKCHAIN_RPC_URL = _env("BLOCKCHAIN_RPC_URL", "")
BLOCKCHAIN_CONTRACT_ADDRESS = _env("BLOCKCHAIN_CONTRACT_ADDRESS", "")

# Logging
LOG_LEVEL = _env("LOG_LEVEL", "INFO")
