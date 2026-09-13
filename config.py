import os
import shutil
import sys
from pathlib import Path
# Tải cấu hình từ .env
BASE_DIR = Path(__file__).resolve().parent

try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / ".env", override=True)
except ImportError:
    # Fallback tự đọc file .env nếu chưa cài thư viện python-dotenv
    env_file = BASE_DIR / ".env"
    if env_file.exists():
        try:
            with open(env_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        k = k.strip()
                        v = v.strip().strip("'\"")
                        if k and k not in os.environ:
                            os.environ[k] = v
        except Exception:
            pass


class Config:
    BASE_DIR: Path = BASE_DIR
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()

    # Danh sách User ID được phép truy cập (Whitelist)
    _allowed_raw: str = os.getenv("ALLOWED_USER_IDS", "").strip()
    ALLOWED_USER_IDS: set[int] = set()
    if _allowed_raw:
        for uid in _allowed_raw.replace(";", ",").split(","):
            uid = uid.strip()
            if uid.isdigit():
                ALLOWED_USER_IDS.add(int(uid))

    # Cấu hình Xác thực & Bảo mật (PIN Authentication & Auto-Lock)
    AUTH_PIN_HASH: str = os.getenv("AUTH_PIN_HASH", "").strip()
    AUTH_MAX_ATTEMPTS: int = int(os.getenv("AUTH_MAX_ATTEMPTS", "5"))
    AUTH_LOCKOUT_SECONDS: int = int(os.getenv("AUTH_LOCKOUT_SECONDS", "300"))
    AUTH_AUTO_LOCK_MINUTES: int = int(os.getenv("AUTH_AUTO_LOCK_MINUTES", "30"))

    # Workspace mặc định
    DEFAULT_WORKSPACE: str = os.getenv(
        "DEFAULT_WORKSPACE", str(BASE_DIR)
    ).strip()

    # Agent mặc định ("antigravity" hoặc "codex")
    DEFAULT_AGENT: str = os.getenv("DEFAULT_AGENT", "antigravity").strip().lower()

    # Cấu hình Antigravity CLI
    DEFAULT_ANTIGRAVITY_MODEL: str = os.getenv(
        "DEFAULT_MODEL", "Gemini 3.7 Flash (High)"
    ).strip()
    DEFAULT_MODEL: str = DEFAULT_ANTIGRAVITY_MODEL  # Giữ tương thích
    DEFAULT_EFFORT: str = os.getenv("DEFAULT_EFFORT", "high").strip()
    DEFAULT_MODE: str = os.getenv("DEFAULT_MODE", "accept-edits").strip()
    TASK_TIMEOUT: int = int(os.getenv("TASK_TIMEOUT", "600"))

    # Cấu hình OpenAI Codex CLI
    DEFAULT_CODEX_MODEL: str = os.getenv(
        "DEFAULT_CODEX_MODEL", "gpt-5.6-terra"
    ).strip()
    DEFAULT_CODEX_EFFORT: str = os.getenv("DEFAULT_CODEX_EFFORT", "medium").strip()

    # Cấu hình Cocos Creator Engine
    COCOS_CREATOR_PATH: str = os.getenv("COCOS_CREATOR_PATH", "").strip()
    COCOS_CREATOR_2X_PATH: str = os.getenv("COCOS_CREATOR_2X_PATH", "").strip()
    COCOS_CREATOR_3X_PATH: str = os.getenv("COCOS_CREATOR_3X_PATH", "").strip()
    DEFAULT_PREVIEW_PORT: int = int(os.getenv("DEFAULT_PREVIEW_PORT", "7456"))

    # Cấu hình Cloudflare Tunnel
    CLOUDFLARED_PATH: str = os.getenv("CLOUDFLARED_PATH", "").strip()
    CLOUDFLARE_MODE: str = os.getenv("CLOUDFLARE_MODE", "quick").strip().lower()
    CLOUDFLARE_TUNNEL_NAME: str = os.getenv("CLOUDFLARE_TUNNEL_NAME", "").strip()
    CLOUDFLARE_HOSTNAME: str = os.getenv("CLOUDFLARE_HOSTNAME", "").strip()

    # Tự động tìm đường dẫn agy (Hỗ trợ cả Windows và Linux)
    _agy_env = os.getenv("AGY_PATH", "").strip()
    if _agy_env and os.path.exists(_agy_env):
        AGY_PATH: str = _agy_env
    else:
        _which_agy = shutil.which("agy") or shutil.which("agy.exe")
        _agy_candidates = [
            _which_agy,
            os.path.expandvars(r"%LOCALAPPDATA%\agy\bin\agy.exe") if sys.platform == "win32" else "",
            str(Path.home() / ".local" / "bin" / "agy"),
            "/usr/local/bin/agy",
            "/usr/bin/agy",
            str(Path.home() / "Applications" / "Antigravity IDE" / "bin" / "agy"),
            str(Path.home() / "Applications" / "Antigravity IDE" / "bin" / "antigravity-ide"),
            str(Path.home() / "Applications" / "Antigravity IDE" / "antigravity-ide"),
            "/opt/Antigravity IDE/bin/agy",
            "/opt/antigravity/bin/agy",
        ]
        AGY_PATH = "agy"
        for c in _agy_candidates:
            if c and os.path.exists(c):
                AGY_PATH = c
                break

    # Tự động tìm đường dẫn codex (Hỗ trợ cả Windows và Linux)
    _codex_env = os.getenv("CODEX_PATH", "").strip()
    if _codex_env and os.path.exists(_codex_env):
        CODEX_PATH: str = _codex_env
    else:
        _which_codex = (
            shutil.which("codex.cmd")
            or shutil.which("codex.exe")
            or shutil.which("codex")
        )
        _codex_candidates = [
            _which_codex,
            os.path.expandvars(r"%APPDATA%\npm\codex.cmd") if sys.platform == "win32" else "",
            os.path.expandvars(r"%LOCALAPPDATA%\OpenAI\Codex\bin\codex.exe") if sys.platform == "win32" else "",
            str(Path.home() / ".npm-global" / "bin" / "codex"),
            str(Path.home() / ".local" / "bin" / "codex"),
            "/usr/local/bin/codex",
            "/usr/bin/codex",
        ]
        CODEX_PATH = "codex"
        for c in _codex_candidates:
            if c and os.path.exists(c):
                CODEX_PATH = c
                break

    # Tự động tìm cloudflared nếu chưa có cấu hình (Hỗ trợ cả Windows và Linux)
    if not CLOUDFLARED_PATH or not os.path.exists(CLOUDFLARED_PATH):
        _cf_candidates = [
            shutil.which("cloudflared") or shutil.which("cloudflared.exe"),
            r"C:\Program Files (x86)\cloudflared\cloudflared.exe" if sys.platform == "win32" else "",
            r"C:\Program Files\cloudflared\cloudflared.exe" if sys.platform == "win32" else "",
            os.path.expandvars(r"%LOCALAPPDATA%\cloudflared\cloudflared.exe") if sys.platform == "win32" else "",
            "/usr/local/bin/cloudflared",
            "/usr/bin/cloudflared",
            str(Path.home() / ".local" / "bin" / "cloudflared"),
        ]
        for c in _cf_candidates:
            if c and os.path.exists(c):
                CLOUDFLARED_PATH = c
                break

    @classmethod
    def reload(cls):
        """Tải lại file .env khi có thay đổi."""
        load_dotenv(BASE_DIR / ".env", override=True)
        cls.TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
        cls._allowed_raw = os.getenv("ALLOWED_USER_IDS", "").strip()
        cls.ALLOWED_USER_IDS = set()
        if cls._allowed_raw:
            for uid in _allowed_raw.replace(";", ",").split(","):
                uid = uid.strip()
                if uid.isdigit():
                    cls.ALLOWED_USER_IDS.add(int(uid))
        cls.AUTH_PIN_HASH = os.getenv("AUTH_PIN_HASH", "").strip()
        cls.AUTH_MAX_ATTEMPTS = int(os.getenv("AUTH_MAX_ATTEMPTS", "5"))
        cls.AUTH_LOCKOUT_SECONDS = int(os.getenv("AUTH_LOCKOUT_SECONDS", "300"))
        cls.AUTH_AUTO_LOCK_MINUTES = int(os.getenv("AUTH_AUTO_LOCK_MINUTES", "30"))
        cls.DEFAULT_WORKSPACE = os.getenv(
            "DEFAULT_WORKSPACE", str(BASE_DIR)
        ).strip()
        cls.DEFAULT_AGENT = os.getenv("DEFAULT_AGENT", "antigravity").strip().lower()
        cls.DEFAULT_ANTIGRAVITY_MODEL = os.getenv(
            "DEFAULT_MODEL", "Gemini 3.7 Flash (High)"
        ).strip()
        cls.DEFAULT_MODEL = cls.DEFAULT_ANTIGRAVITY_MODEL
        cls.DEFAULT_CODEX_MODEL = os.getenv(
            "DEFAULT_CODEX_MODEL", "gpt-5.6-terra"
        ).strip()
        cls.DEFAULT_EFFORT = os.getenv("DEFAULT_EFFORT", "high").strip()
        cls.DEFAULT_MODE = os.getenv("DEFAULT_MODE", "accept-edits").strip()
        cls.COCOS_CREATOR_PATH = os.getenv("COCOS_CREATOR_PATH", "").strip()
        cls.COCOS_CREATOR_2X_PATH = os.getenv("COCOS_CREATOR_2X_PATH", "").strip()
        cls.COCOS_CREATOR_3X_PATH = os.getenv("COCOS_CREATOR_3X_PATH", "").strip()
        cls.CLOUDFLARED_PATH = os.getenv("CLOUDFLARED_PATH", "").strip()
        cls.CLOUDFLARE_MODE = os.getenv("CLOUDFLARE_MODE", "quick").strip().lower()
        cls.CLOUDFLARE_TUNNEL_NAME = os.getenv("CLOUDFLARE_TUNNEL_NAME", "").strip()
        cls.CLOUDFLARE_HOSTNAME = os.getenv("CLOUDFLARE_HOSTNAME", "").strip()

    @classmethod
    def is_user_allowed(cls, user_id: int) -> bool:
        """Kiểm tra quyền truy cập của người dùng theo danh sách Whitelist."""
        if not cls.ALLOWED_USER_IDS:
            return False
        return user_id in cls.ALLOWED_USER_IDS
