FROM debian:bullseye-slim

VOLUME /app/
WORKDIR /app/
ENV DS_CONFIG='docker'
ENV DS_APP_PORT='5000'
ENV DS_LOG_DIR='/app/logs'
ENV DS_TMP_DIR='/tmp/'
ENV B2_KEY_ID=''
ENV B2_KEY_SECRET=''
ENV B2_APP_BUCKET=''
ENV B2_APP_NAME=''
ENV SLACK_TOKEN=''

ADD ./src /app

# Install apt requirements
RUN apt-get update && \
    apt-get install -y \
        python3-dev \
        libpython3-dev \
        python3-pip \
        procps \
        git

RUN pip3 install -r /app/requirements.txt

CMD tail -f /dev/null