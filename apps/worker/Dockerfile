FROM python:3.11-slim

ENV POETRY_VERSION=1.8.3
WORKDIR /app

RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*
RUN pip install "poetry==$POETRY_VERSION"
COPY pyproject.toml poetry.lock* ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root
COPY src ./src
COPY pipelines ./pipelines
COPY scripts ./scripts
COPY entrypoint.sh ./entrypoint.sh
RUN chmod +x entrypoint.sh
CMD ["./entrypoint.sh"]
