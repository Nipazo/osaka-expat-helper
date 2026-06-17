# 🏯 Osaka Expat Helper

**Osaka Expat Helper** — это локальный веб-сервис для экспатов в Японии.  
Он помогает переводить официальные письма из японской мэрии (сложные иероглифы) на **английский** и **русский** языки.

---

## 🚀 Возможности

- 📸 Загрузка фото официального письма (квитанции, уведомления, страховки)
- 🔍 Распознавание японского текста (Tesseract OCR)
- 🇯🇵 → 🇬🇧 Перевод на английский
- 🇯🇵 → 🇷🇺 Перевод на русский
- 📋 Краткое резюме сути документа
- ✅ Выделение ключевых действий (оплатить, подать, обновить)
- ⏰ Определение дедлайнов
- 💾 Скачивание переводов в .txt

---

## 🧠 Как это работает
📸 Фото документа
↓
🖥️ Tesseract OCR (распознавание текста)
↓
🧠 Helsinki-NLP (перевод JA → EN + JA → RU)
↓
📊 Извлечение дат и ключевых слов
↓
📱 Отображение перевода в Streamlit

---

## 🛠️ Технологии

| Компонент | Технология |
|-----------|------------|
| Бэкенд | FastAPI |
| Фронтенд | Streamlit |
| OCR | Tesseract |
| Перевод | Helsinki-NLP (opu s-mt-ja-en / opus-mt-ja-ru) |
| Язык | Python 3.10+ |

---

## 📦 Установка и запуск

### 1. Установите Tesseract OCR

Скачайте с [официального сайта](https://github.com/UB-Mannheim/tesseract/wiki)  
**Важно:** при установке отметьте **Japanese language**

### 2. Клонируйте репозиторий

```bash
git clone https://github.com/Nipazo/osaka-expat-helper.git
cd osaka-expat-helper

Создайте виртуальное окружение
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate # Linux/Mac

Установите зависимости
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt

Запустите бэкенд
python backend/app.py

Откройте браузер
http://localhost:8501
