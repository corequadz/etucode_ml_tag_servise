# Используем легковесный базовый образ
FROM python:3.11-slim

WORKDIR /app

# 1. Ставим системные компиляторы
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 2. Принудительно ставим ЛЕГКУЮ CPU-версию PyTorch (с таймаутом и ретраями)
RUN pip install --default-timeout=2000 --retries 10 --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# 3. Ставим остальные зависимости
RUN pip install --default-timeout=2000 --retries 10 --no-cache-dir fastapi uvicorn pydantic transformers sentence-transformers scipy

# 4. Копируем исходный код
COPY . .

# 5. Прогрев кэша: скачиваем веса модели на этапе сборки
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('cointegrated/rubert-tiny2')"

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]