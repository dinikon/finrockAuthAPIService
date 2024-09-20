# Используем официальный образ Python как базовый
FROM python:3.12-slim
LABEL authors="inikon"

# Устанавливаем рабочую директорию в контейнере
WORKDIR /finrockAuthAPI

# Копируем зависимости
COPY ./app/requirements.txt /finrockAuthAPI/requirements.txt

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r /finrockAuthAPI/requirements.txt

# Копируем остальные файлы проекта
COPY ./app /finrockAuthAPI/

# Указываем порт, который будет слушать контейнер
EXPOSE 8000

# Запускаем FastAPI приложение
CMD ["uvicorn", "main:main_app", "--host", "0.0.0.0", "--port", "8000"]
