FROM python:3.11.7

WORKDIR /app

COPY . /app/

RUN apt-get update && apt-get install -y \
    libzbar0 \
    poppler-utils
RUN pip install --no-cache-dir -r requirements.txt

RUN groupadd -r checkergroup && useradd -r -g checkergroup checker
RUN chown -R checker:checkergroup /app
USER checker


CMD ["python3", "-u", "checker.py"]