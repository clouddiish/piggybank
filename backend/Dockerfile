FROM python:3.13.2

WORKDIR /backend
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt 

COPY . .

RUN chmod +x entrypoint.sh && \
    apt-get update && apt-get install -y postgresql-client


EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
