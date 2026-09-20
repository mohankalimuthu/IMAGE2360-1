import os
from dotenv import load_dotenv


load_dotenv()


# -----------------------------------------
# WithoutBG
# -----------------------------------------

WITHOUTBG_API_KEY = os.getenv(
    "WITHOUTBG_API_KEY"
)


WITHOUTBG_CAR_URL = (
    "https://api.withoutbg.com"
    "/v1.0/car-image-without-background"
)


# -----------------------------------------
# Directories
# -----------------------------------------

UPLOAD_DIR = "uploads"

OUTPUT_DIR = "outputs"


# -----------------------------------------
# File validation
# -----------------------------------------

MAX_FILE_SIZE_MB = 20


ALLOWED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".avif",
    ".heic",
    ".tiff",
    ".bmp",
    ".gif"
}