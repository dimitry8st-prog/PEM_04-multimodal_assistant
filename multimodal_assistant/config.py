import os
import logging
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

logger = logging.getLogger(__name__)


class Settings(BaseModel):
    """Настройки приложения"""
    # OpenAI
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_api_base: str | None = os.getenv("OPENAI_API_BASE")

    # Models
    text_model: str = "gpt-4o-mini"
    vision_model: str = "gpt-4o-mini"
    whisper_model: str = "whisper-1"
    tts_model: str = "tts-1"
    image_model: str = "dall-e-3"

    # Telegram
    telegram_bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    telegram_bot_token_voice: str = os.getenv("TELEGRAM_BOT_TOKEN_VOICE", "")
    telegram_bot_token_image: str = os.getenv("TELEGRAM_BOT_TOKEN_IMAGE", "")
    telegram_bot_token_product: str = os.getenv("TELEGRAM_BOT_TOKEN_PRODUCT", "")


settings = Settings()
logger.info("Конфигурация загружена")
