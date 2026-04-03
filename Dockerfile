FROM python:3.10-slim

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip setuptools wheel

COPY pyproject.toml .
COPY uv.lock .
COPY MANIFEST.in .
COPY README.md .
COPY openenv.yaml .
COPY app.py .
COPY inference.py .
COPY src/ ./src/
COPY supply_chain_env/ ./supply_chain_env/
COPY scripts/ ./scripts/
COPY server/ ./server/

RUN pip install --no-cache-dir .

EXPOSE 7860

CMD ["server", "--host", "0.0.0.0", "--port", "7860"]
