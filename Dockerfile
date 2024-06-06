FROM python:3.10-slim

WORKDIR /usr/src/app

RUN pip3 install aiohttp

COPY . .

CMD [ "python", "./Main.py" ]
