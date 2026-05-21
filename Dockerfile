FROM python:3.12-slim

LABEL maintainer="Chaîne d'automatisation"
LABEL project="Infrastructure Kubernetes sécurisée supervisée automatisée"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --root-user-action=ignore -r requirements.txt \
    && useradd -u 1000 -m appuser \
    && chown -R appuser:appuser /app

COPY app/ ./app/
RUN chown -R appuser:appuser /app

EXPOSE 8080

USER appuser

CMD ["python", "app/main.py"]
