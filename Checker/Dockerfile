FROM python:3.11.7

WORKDIR /app

COPY . /app/

RUN apt-get update && apt-get install -y \
    libzbar0 \
    poppler-utils
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "-u", "checker.py"]