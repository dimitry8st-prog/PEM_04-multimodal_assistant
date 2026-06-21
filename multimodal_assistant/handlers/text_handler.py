import logging
import threading

from telebot.types import Message

from openai_client import chat_completion, run_async

logger = logging.getLogger(__name__)


def handle_text(bot, message: Message) -> None:
    """Обработка текстовых сообщений"""
    if message.text.startswith('/'):
        return

    logger.info(f"Получено текстовое сообщение от пользователя {message.chat.id}")

    threading.Thread(
        target=_process_text,
        args=(bot, message),
        daemon=True
    ).start()


def _process_text(bot, message: Message):
    """Внутренняя функция обработки текста"""
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        response = run_async(chat_completion([
            {"role": "user", "content": message.text}
        ]))
        bot.send_message(message.chat.id, response)
        logger.info(f"Текстовый ответ отправлен пользователю {message.chat.id}")

    except Exception as e:
        logger.error(f"Ошибка при обработке текста: {e}", exc_info=True)
        bot.send_message(message.chat.id, f"❌ Ошибка: {str(e)}")
