import os.path
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DEBUG = False
ADS_POWER_API_URL = "http://localhost:50325"

MEDIA_FOLDER = BASE_DIR / "media"
SPAM_TIMEOUT = 1  # minutes in code will be multiplied by 60

if not os.path.exists(MEDIA_FOLDER):
    os.mkdir(MEDIA_FOLDER)
