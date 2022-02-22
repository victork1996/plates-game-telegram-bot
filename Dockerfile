FROM python:latest

WORKDIR /bot
ADD . .

RUN pip install -r requirements.txt
CMD ["sh", "-c", "python bot.py data/cars.db $TOKEN"]