# Используем базовый образ Python
FROM python:3.10-slim

# Устанавливаем переменную окружения для отображения вывода в консоли
ENV PYTHONUNBUFFERED 1

# Устанавливаем рабочую директорию в /app
WORKDIR /app

# Копируем зависимости в контейнер
COPY requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/

CMD ["python3", "main.py"]
