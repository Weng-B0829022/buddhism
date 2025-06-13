FROM python:3.11
WORKDIR /app

RUN apt-get update && apt-get install -y \
    ffmpeg \
    build-essential \
    python3-dev

RUN pip install --upgrade pip setuptools wheel

COPY backend/requirements.txt .
COPY backend/*.whl .
RUN pip install -r requirements.txt
RUN pip install avatar_sync_lip-1.0.1-py3-none-any.whl
RUN pip install voice_api-2.0.0-py3-none-any.whl
COPY backend/ .
EXPOSE 8001
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]