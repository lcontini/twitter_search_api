# docker build -f deploy/docker/Dockerfile -t twitter_api .
FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./twitter_api_main.py" ]