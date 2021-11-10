FROM python:3.9-slim
WORKDIR /inventory

# install dependencies
RUN pip install -U pipenv
COPY Pipfile* ./

RUN apt-get update && apt-get install -y \
        libssl-dev \
        libffi-dev \
        g++ \
        tzdata \
    && ln -fs /usr/share/zoneinfo/Europe/Moscow /etc/localtime \
    && pipenv install --system --deploy \
    && rm -rf /var/cache/apt/*

COPY . .

