import logging
import threading

from telebot.types import Message

from openai_client import analyze_image, generate_image, run_async
from utils.file_utils import download_file_as_bytes
from utils.prompts import IMAGE_PROMPT_TEMPLATE_RU

logger = logging.getLogger(__name__)


def handle_image(bot, message: Message) -> None:
    """Обработка изображений: анализ или генерация"""
    if message.photo:
        logger.info(f"Получено изображение от пользователя {message.chat.id}")
        threading.Thread(
            target=_process_image_analysis,
            args=(bot, message),
            daemon=True
        ).start()

    elif message.text and message.text.startswith('/generate'):
        prompt = message.text.replace('/generate', '').strip()
        if not prompt:
            bot.send_message(message.chat.id, "Использование: /generate [описание изображения]")
            return

        logger.info(f"Запрос на генерацию изображения от пользователя {message.chat.id}")
        threading.Thread(
            target=_process_image_generation,
            args=(bot, message, prompt),
            daemon=True
        ).start()


def _process_image_analysis(bot, message: Message):
    """Внутренняя функция анализа изображения"""
    try:
        photo = message.photo[-1]
        bot.send_message(message.chat.id, "🖼️ Анализирую изображение...")
        file_bytes = download_file_as_bytes(bot, photo.file_id)
        analysis = run_async(analyze_image(file_bytes))

        bot.send_message(
            message.chat.id,
            f"🔍 **Анализ изображения:**\n\n{analysis}",
            parse_mode="Markdown"
        )
        logger.info(f"Анализ изображения завершен для пользователя {message.chat.id}")

    except Exception as e:
        logger.error(f"Ошибка при анализе изображения: {e}", exc_info=True)
        bot.send_message(message.chat.id, f"❌ Ошибка при анализе изображения: {str(e)}")


def _process_image_generation(bot, message: Message, prompt: str):
    """Внутренняя функция генерации изображения"""
    try:
        bot.send_message(message.chat.id, "🎨 Генерирую изображение... Это может занять 10-30 секунд.")
        image_url = run_async(generate_image(prompt))

        bot.send_photo(
            message.chat.id,
            image_url,
            caption=f"✅ Изображение сгенерировано:\n{prompt}"
        )
        logger.info(f"Генерация изображения завершена для пользователя {message.chat.id}")

    except Exception as e:
        logger.error(f"Ошибка при генерации изображения: {e}", exc_info=True)
        bot.send_message(message.chat.id, f"❌ Ошибка при генерации изображения: {str(e)}")
