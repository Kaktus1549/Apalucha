FROM python:3.11.7

WORKDIR /app

COPY . /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "-u", "checker.py"]