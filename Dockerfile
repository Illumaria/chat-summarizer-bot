FROM python:3.8.12-slim

EXPOSE 8080

COPY ./secure-connect-chat-summarizer-bot.zip secure-connect-chat-summarizer-bot.zip

COPY ./requirements.txt requirements.txt
RUN python -m pip install --upgrade pip && \
    python -m pip install -r requirements.txt

COPY ./src src
COPY ./bot.py bot.py

ENTRYPOINT ["python", "bot.py"]