import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def is_pdf(file_path: str) -> bool:
    """Проверяет, является ли файл PDF"""
    return file_path.lower().endswith('.pdf')


def is_image(file_path: str) -> bool:
    """Проверяет, является ли файл изображением"""
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    return any(file_path.lower().endswith(ext) for ext in image_extensions)


def download_file_as_bytes(bot, file_id: str) -> bytes:
    """Скачивает файл из Telegram и возвращает байты"""
    logger.info(f"Скачивание файла с ID: {file_id}")
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    logger.info(f"Файл скачан, размер: {len(downloaded_file)} байт")
    return downloaded_file


def save_file_to_temp(file_bytes: bytes, filename: str) -> str:
    """Сохраняет файл во временную папку"""
    temp_dir = Path("temp")
    temp_dir.mkdir(exist_ok=True)
    file_path = temp_dir / filename
    with open(file_path, 'wb') as f:
        f.write(file_bytes)
    logger.info(f"Файл сохранен: {file_path}")
    return str(file_path)


def cleanup_temp_file(file_path: str):
    """Удаляет временный файл"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Временный файл удален: {file_path}")
    except Exception as e:
        logger.error(f"Ошибка при удалении файла {file_path}: {e}")


def format_analysis_report(data: dict) -> str:
    """Форматирует данные анализа в текстовый отчёт"""
    if isinstance(data, str):
        return data

    report = []
    for key, value in data.items():
        if isinstance(value, list):
            report.append(f"**{key}**:")
            for item in value:
                report.append(f"  • {item}")
        else:
            report.append(f"**{key}**: {value}")

    return "\n".join(report)


def extract_text_from_pdf(pdf_path: str) -> str:
    """Извлекает текст из PDF файла"""
    from PyPDF2 import PdfReader
    logger.info(f"Извлечение текста из PDF: {pdf_path}")
    text = ""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
    logger.info(f"Извлечено {len(text)} символов")
    return text
