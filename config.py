import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL = "gemini-2.5-flash"

    RATE_LIMIT_PER_MINUTE = 10
    MAX_MESSAGE_LENGTH = 500

    DATA_FILE = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "data",
        "opportunities.json",
    )

    LOG_FILE = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "logs",
        "app.log",
    )

    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-in-production")
