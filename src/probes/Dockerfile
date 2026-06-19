FROM python:3.11-slim

RUN apt-get update && apt-get install -y iputils-ping && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Correct the path location inside the 'src/' build context
COPY probes/network_probe.py .

ENV PYTHONUNBUFFERED=1

CMD ["python", "network_probe.py"]
