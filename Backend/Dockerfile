FROM python:3.11.7

RUN groupadd -r backendgroup && useradd -r -g backendgroup backend

WORKDIR /app

COPY . /app/

RUN pip install --no-cache-dir -r requirements.txt

RUN chown -R backend:backendgroup /app

USER backend

EXPOSE 5000

CMD ["python3", "main.py"]