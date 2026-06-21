import asyncio
import base64
import logging
from io import BytesIO
from typing import Dict, List

from openai import AsyncOpenAI
from PyPDF2 import PdfReader

from config import settings
from utils.prompts import (
    GENERAL_ASSISTANT_SYSTEM_PROMPT_RU,
    TEXT_DOCUMENT_ANALYSIS_PROMPT_RU,
    VISION_ANALYSIS_PROMPT_RU,
)

logger = logging.getLogger(__name__)


def _build_client() -> AsyncOpenAI:
    if settings.openai_api_base:
        return AsyncOpenAI(
            api_key=settings.openai_api_key,
            base_url=settings.openai_api_base
        )
    return AsyncOpenAI(api_key=settings.openai_api_key)


client = _build_client()
logger.info("OpenAI клиент инициализирован")


async def analyze_document(pdf_bytes: bytes, prompt: str = TEXT_DOCUMENT_ANALYSIS_PROMPT_RU) -> str:
    """Анализирует PDF документ"""
    logger.info("Начало анализа PDF документа")
    pdf_file = BytesIO(pdf_bytes)
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    logger.info(f"Извлечено {len(text)} символов из PDF")

    response = await client.chat.completions.create(
        model=settings.text_model,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": text}
        ],
        temperature=0.2
    )
    result = response.choices[0].message.content
    logger.info("Анализ PDF завершен")
    return result


async def analyze_image(image_bytes: bytes, prompt: str = VISION_ANALYSIS_PROMPT_RU) -> str:
    """Анализирует изображение"""
    logger.info("Начало анализа изображения")
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')

    response = await client.chat.completions.create(
        model=settings.vision_model,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        }
                    }
                ]
            }
        ],
        temperature=0.2
    )
    result = response.choices[0].message.content
    logger.info("Анализ изображения завершен")
    return result


async def generate_image(prompt: str) -> str:
    """Генерирует изображение по текстовому описанию"""
    logger.info(f"Генерация изображения по промпту: {prompt[:50]}...")
    response = await client.images.generate(
        model=settings.image_model,
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    result = response.data[0].url
    logger.info("Генерация изображения завершена")
    return result


async def transcribe_audio(audio_bytes: bytes) -> str:
    """Расшифровывает голосовое сообщение"""
    logger.info("Начало расшифровки аудио")
    audio_file = BytesIO(audio_bytes)
    audio_file.name = "voice.ogg"

    response = await client.audio.transcriptions.create(
        model=settings.whisper_model,
        file=audio_file,
        language="ru"
    )
    result = response.text
    logger.info(f"Расшифровка завершена, текст: {result[:50]}...")
    return result


async def text_to_speech(text: str) -> bytes:
    """Преобразует текст в речь"""
    logger.info(f"Начало синтеза речи, длина текста: {len(text)}")
    response = await client.audio.speech.create(
        model=settings.tts_model,
        voice="alloy",
        input=text
    )
    result = response.content
    logger.info("Синтез речи завершен")
    return result


async def chat_completion(messages: List[Dict[str, str]]) -> str:
    """Общее общение с моделью"""
    logger.info("Начало генерации ответа")
    response = await client.chat.completions.create(
        model=settings.text_model,
        messages=[
            {"role": "system", "content": GENERAL_ASSISTANT_SYSTEM_PROMPT_RU},
            *messages
        ],
        temperature=0.2
    )
    result = response.choices[0].message.content
    logger.info("Генерация ответа завершена")
    return result


async def generate_voice_answer(text: str) -> bytes:
    """Генерирует голосовой ответ на текст"""
    return await text_to_speech(text)


def run_async(coro):
    """Запускает асинхронную функцию в синхронном контексте"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()
