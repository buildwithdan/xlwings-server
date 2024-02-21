FROM python:3.12-slim

# Makes sure that logs are shown immediately
ENV PYTHONUNBUFFERED=1

COPY ./requirements.in .
COPY ./requirements.txt .
# Watchfiles from uvicorn[standard] breaks reload inside Docker so must be removed
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app

EXPOSE 8000

WORKDIR /app

WORKDIR /

# This is for single-container deployments (multiple-workers)
CMD ["gunicorn", "app.main:cors_app", \
     "--bind", "0.0.0.0:8000", \
     "--access-logfile", "-", \
     "--workers", "2", \
     "--worker-class", "uvicorn.workers.UvicornWorker"]