import logging
import threading
from io import BytesIO

from telebot.types import Message

from openai_client import transcribe_audio, chat_completion, generate_voice_answer, run_async
from utils.file_utils import download_file_as_bytes

logger = logging.getLogger(__name__)


def handle_voice(bot, message: Message) -> None:
    """Обработка голосовых сообщений"""
    logger.info(f"Получено голосовое сообщение от пользователя {message.chat.id}")

    threading.Thread(
        target=_process_voice,
        args=(bot, message),
        daemon=True
    ).start()


def _process_voice(bot, message: Message):
    """Внутренняя функция обработки голоса"""
    try:
        bot.send_message(message.chat.id, "🎤 Обрабатываю голосовое сообщение...")
        audio_bytes = download_file_as_bytes(bot, message.voice.file_id)

        text = run_async(transcribe_audio(audio_bytes))
        bot.send_message(message.chat.id, f"📝 Распознанный текст: {text}")

        response = run_async(chat_completion([
            {"role": "user", "content": text}
        ]))
        bot.send_message(message.chat.id, f"💬 Ответ: {response}")

        bot.send_message(message.chat.id, "🔊 Генерирую голосовой ответ...")
        voice_bytes = run_async(generate_voice_answer(response))
        voice_file = BytesIO(voice_bytes)
        voice_file.name = "response.ogg"
        bot.send_voice(message.chat.id, voice_file)

        logger.info(f"Голосовая обработка завершена для пользователя {message.chat.id}")

    except Exception as e:
        logger.error(f"Ошибка при обработке голосового сообщения: {e}", exc_info=True)
        bot.send_message(message.chat.id, f"❌ Ошибка при обработке голосового сообщения: {str(e)}")
