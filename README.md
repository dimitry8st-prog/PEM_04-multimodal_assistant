# 🤖 Мультимодальный AI-ассистент

Универсальный Telegram-бот с поддержкой различных типов контента: PDF-документов, изображений, текста и голосовых сообщений.

## 🌟 Возможности

### 📄 Анализ PDF-документов
- Загрузка и обработка PDF файлов
- Извлечение и анализ текста
- Генерация структурированных отчётов
- Создание голосовых ответов

### 🖼️ Работа с изображениями
- **Анализ**: отправьте фото для детального описания
- **Генерация**: используйте `/generate [описание]` для создания изображений с помощью DALL-E 3

### 💬 Текстовое общение
- Ответы на вопросы
- Помощь с задачами
- Поддержка контекста разговора

### 🎤 Голосовые сообщения
- Распознавание речи (Speech-to-Text)
- Текстовые ответы
- Голосовые ответы (Text-to-Speech)

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
cd multimodal_assistant
pip install -r requirements.txt
```

### 2. Настройка переменных окружения

Скопируйте `.env.example` в `.env`:

```bash
cp .env.example .env
```

Откройте `.env` и укажите свои данные:

```env
OPENAI_API_KEY=sk-proj-your_key_here
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

### 3. Получение API ключей

#### OpenAI API Key
1. Перейдите на [platform.openai.com](https://platform.openai.com)
2. Создайте новый API ключ

#### Telegram Bot Token
1. Найдите [@BotFather](https://t.me/BotFather) в Telegram
2. Отправьте `/newbot`
3. Скопируйте полученный токен

### 4. Запуск бота

```bash
python main.py
```

## 📁 Структура проекта

```
multimodal_assistant/
├── handlers/
│   ├── __init__.py
│   ├── pdf_handler.py
│   ├── image_handler.py
│   ├── text_handler.py
│   └── voice_handler.py
├── utils/
│   ├── __init__.py
│   ├── file_utils.py
│   └── prompts.py
├── config.py
├── openai_client.py
├── main.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## 🛠️ Технологии

- **Python 3.10+**
- **pyTelegramBotAPI** - Telegram API
- **OpenAI API** - AI модели (GPT-4o-mini, Whisper-1, TTS-1, DALL-E 3)
- **PyPDF2** - работа с PDF
- **python-dotenv** - переменные окружения
- **pydantic** - валидация конфигурации

## ⚙️ Конфигурация

### Модели AI

В `config.py`:

```python
text_model: str = "gpt-4o-mini"
vision_model: str = "gpt-4o-mini"
whisper_model: str = "whisper-1"
tts_model: str = "tts-1"
image_model: str = "dall-e-3"
```

### Temperature

Установлена `temperature=0.2` для всех генераций текста для более точных и детерминированных ответов.

## 📋 Логгирование

Логи записываются в файл `bot.log` и выводятся в консоль. Формат:

```
2024-01-01 12:00:00 - module_name - INFO - Сообщение
```

## 🔒 Безопасность

- Никогда не публикуйте `.env` с реальными ключами
- Добавьте `.env` в `.gitignore`

## 🐛 Решение проблем

### Бот не запускается
- Проверьте токен в `.env`
- Установите зависимости: `pip install -r requirements.txt`

### Ошибки API
- Проверьте баланс OpenAI API
- Убедитесь, что ключ активен

## Лицензия

Учебный проект (PEM04 multimodal_assistant). Свободное использование в рамках задания.