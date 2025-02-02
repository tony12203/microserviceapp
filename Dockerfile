FROM python:3.9-slim

WORKDIR /app
COPY . .

COPY requirements.txt .
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt

CMD ["python", "app.py"]
