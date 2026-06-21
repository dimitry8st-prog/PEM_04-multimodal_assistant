import logging
import telebot
from telebot import types

from config import settings
from handlers.pdf_handler import handle_pdf
from handlers.image_handler import handle_image
from handlers.text_handler import handle_text
from handlers.voice_handler import handle_voice

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

bot = telebot.TeleBot(settings.telegram_bot_token)

WELCOME_MESSAGE = """👋 Привет! Я мультимодальный AI-ассистент.

Мои возможности:

📄 **PDF-документы** - отправь PDF файл, и я проанализирую его содержимое

🖼️ **Изображения** - отправь фото для анализа или используй /generate для создания

💬 **Текст** - просто напиши мне, и я отвечу

🎤 **Голос** - отправь голосовое сообщение, и я отвечу голосом

Команды:
/start - показать это сообщение
/generate [описание] - создать изображение
/help - помощь"""


@bot.message_handler(commands=['start'])
def send_welcome(message: types.Message):
    """Обработчик команды /start"""
    logger.info(f"Команда /start от пользователя {message.chat.id}")
    bot.send_message(message.chat.id, WELCOME_MESSAGE, parse_mode="Markdown")


@bot.message_handler(commands=['help'])
def send_help(message: types.Message):
    """Обработчик команды /help"""
    logger.info(f"Команда /help от пользователя {message.chat.id}")
    bot.send_message(message.chat.id, WELCOME_MESSAGE, parse_mode="Markdown")


@bot.message_handler(content_types=['document'])
def handle_document(message: types.Message):
    """Обработчик документов"""
    handle_pdf(bot, message)


@bot.message_handler(content_types=['photo'])
def handle_photo(message: types.Message):
    """Обработчик фотографий"""
    handle_image(bot, message)


@bot.message_handler(content_types=['voice'])
def handle_voice_message(message: types.Message):
    """Обработчик голосовых сообщений"""
    handle_voice(bot, message)


@bot.message_handler(content_types=['text'])
def handle_text_message(message: types.Message):
    """Обработчик текстовых сообщений"""
    handle_text(bot, message)


def main():
    """Запуск бота"""
    logger.info("Бот запускается")
    print("✅ Бот запущен и готов к работе!")
    print(f"🤖 Bot token: {settings.telegram_bot_token[:10]}...")
    print("📝 Поддерживается параллельная обработка запросов")
    print("📋 Логи записываются в файл bot.log")
    bot.infinity_polling(timeout=60, long_polling_timeout=60)


if __name__ == "__main__":
    main()
