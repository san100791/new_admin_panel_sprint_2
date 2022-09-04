FROM python:3.10

# папка внутри контейнера в которой лежат файлы проекта
WORKDIR /opt/app
RUN mkdir /opt/app/static

# создаем пользователя
RUN groupadd -r san && useradd -d /opt/app -r -g san san \
    && chown san:san -R /opt/app

COPY requirements.txt requirements.txt

# установка зависимостей
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

RUN apt-get update

# копируем остальные файлы
COPY . .

EXPOSE 8000

# запуск gunicorn
ENTRYPOINT ["/usr/local/bin/gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]