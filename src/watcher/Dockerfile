FROM python:3.11-slim

WORKDIR /app

COPY watcher/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

ENV PYTHONUNBUFFERED=1

# Tell Python to execute the watcher module while keeping /app/ as the root path lookup
CMD ["python", "-m", "watcher.watcher"]
