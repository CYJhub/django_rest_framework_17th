# pyhton 3.8.3 버전을 담은 이미지를 개조해서 사용할 예정
FROM python:3.8.3-alpine
ENV PYTHONUNBUFFERED 1

# 이미지 내에서 명령어를 실행할 디렉토리 설정
RUN mkdir /app
WORKDIR /app

# dependencies for psycopg2-binary
RUN apk add --no-cache mariadb-connector-c-dev
RUN apk update && apk add python3 python3-dev mariadb-dev build-base && pip3 install mysqlclient && apk del python3-dev mariadb-dev build-base


# By copying over requirements first, we make sure that Docker will cache
# our installed requirements rather than reinstall them on every build
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Now copy in our code, and run it
COPY . /app/