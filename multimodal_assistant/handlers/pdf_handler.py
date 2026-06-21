import logging
import threading
from io import BytesIO

from telebot.types import Message

from openai_client import analyze_document, generate_voice_answer, run_async
from utils.file_utils import download_file_as_bytes

logger = logging.getLogger(__name__)


def handle_pdf(bot, message: Message) -> None:
    """
    Обработка PDF-документов:
    - анализ содержимого,
    - текстовый отчёт + голосовой файл.
    """
    document = message.document
    if document is None:
        return

    if document.mime_type != "application/pdf":
        bot.send_message(message.chat.id, "Пока что я обрабатываю только PDF-документы.")
        return

    logger.info(f"Получен PDF файл от пользователя {message.chat.id}")

    threading.Thread(
        target=_process_pdf,
        args=(bot, message),
        daemon=True
    ).start()


def _process_pdf(bot, message: Message):
    """Внутренняя функция обработки PDF"""
    try:
        bot.send_message(message.chat.id, "📄 Анализирую PDF-документ...")
        document = message.document
        file_bytes = download_file_as_bytes(bot, document.file_id)
        analysis = run_async(analyze_document(file_bytes))

        bot.send_message(
            message.chat.id,
            f"📊 **Анализ документа:**\n\n{analysis}",
            parse_mode="Markdown"
        )

        bot.send_message(message.chat.id, "🔊 Генерирую голосовой ответ...")
        voice_bytes = run_async(generate_voice_answer(analysis))
        voice_file = BytesIO(voice_bytes)
        voice_file.name = "answer.ogg"
        bot.send_voice(message.chat.id, voice_file)

        logger.info(f"PDF обработка завершена для пользователя {message.chat.id}")

    except Exception as e:
        logger.error(f"Ошибка при обработке PDF: {e}", exc_info=True)
        bot.send_message(message.chat.id, f"❌ Ошибка при обработке PDF: {str(e)}")
