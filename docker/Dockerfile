FROM python:3.11.14-alpine

ENV FLASK_APP=app.py \
    FLASK_DEBUG=True \
    RUNTIME_MODE=dev

WORKDIR /app

COPY src/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

COPY src .

RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]

#CMD ["tail", "-f", "/dev/null"]

