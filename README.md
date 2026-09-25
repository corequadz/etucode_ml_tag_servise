# Tag Service API

Микросервис для семантического анализа текста и автоматического присвоения тегов.

## 🚀 Запуск через Docker

1. Сборка образа (веса модели скачиваются на этом этапе):
```bash
docker build -t tag-service .

```

2. Запуск контейнера. **Важно:** Обязательно запускайте контейнер с флагом `-m 2g`, чтобы гарантировать работу в рамках выделенных хард-лимитов (в рабочем режиме потребление составит ~600-800 МБ):

```bash
docker run -d --name tag-api -p 8000:8000 -m 2g tag-service

```

Сервис будет доступен по адресу: `http://localhost:8000`

Интерактивная документация (Swagger): `http://localhost:8000/docs`

---

## 🛠️ Локальный запуск (для разработки)

1. Создайте и активируйте виртуальное окружение:

```bash
python3 -m venv venv
source venv/bin/activate

```

2. Установите зависимости (с увеличенным таймаутом для стабильной загрузки PyTorch):

```bash
pip install --default-timeout=1000 fastapi uvicorn pydantic transformers torch sentence-transformers scipy

```

3. Запустите сервер:

```bash
uvicorn main:app --reload

```

---

## 📡 API Контракт

### 1. Присвоение тегов

**POST** `/api/v1/tags/assign`

**Пример запроса:**

```bash
curl -X POST "[http://127.0.0.1:8000/api/v1/tags/assign](http://127.0.0.1:8000/api/v1/tags/assign)" \
-H "Content-Type: application/json" \
-d '{"message": "У кого можно взять дрель на вечер?"}'

```

**Пример ответа (200 OK):**

```json
{
  "data": [
    "аренда",
    "дрель",
    "инструменты"
  ]
}

```

### 2. Healthcheck (Проверка жизнеспособности)

**GET** `/health`

Используется оркестраторами (например, Docker/Kubernetes) для Liveness-проб.

**Пример запроса:**

```bash
curl -X GET "[http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)"

```

**Пример ответа (200 OK):**

```json
{
  "status": "ok"
}

```

```

```
