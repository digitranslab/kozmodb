FROM python:3.12-slim

LABEL org.opencontainers.image.name="kozmodb/kozmemory-mcp"

WORKDIR /usr/src/kozmemory

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY config.json .
COPY . .

EXPOSE 8765
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8765"]
