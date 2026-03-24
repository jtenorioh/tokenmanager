FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir fastapi uvicorn python-dotenv requests aiofiles

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7776

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7776"]
