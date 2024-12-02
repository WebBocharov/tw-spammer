import os.path
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DEBUG = False
ADS_POWER_API_URL = "http://localhost:50325"

MEDIA_FOLDER = BASE_DIR / "media"
SESSIONS_FOLDER = BASE_DIR / "sessions"

PROXY_REGEX = r'^(http:\/\/)([^:\/\s]+):(\d+)@([^:\/\s]+):([^\/\s]+)$'

SPAM_TIMEOUT = 1  # minutes in code will be multiplied by 60
HEADLESS_MODE = 0

DEFAULT_TEXT = """🔥 HIT MY PIN

⛔️ Don’t SKIP ⛔️

❗️ I CHECK ❗️"""

if not os.path.exists(MEDIA_FOLDER):
    os.mkdir(MEDIA_FOLDER)

if not os.path.exists(SESSIONS_FOLDER):
    os.mkdir(SESSIONS_FOLDER)
