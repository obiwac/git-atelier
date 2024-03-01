FROM python:3

RUN apt install git npm
RUN npm install -g @marp-team/marp-cli
RUN marp presentation.md

WORKDIR /app

#COPY requirements.txt .
#RUN pip install -r requirements.txt

COPY . .

ARG REPO_COUNT
ENV REPO_COUNT=${REPO_COUNT:-10}
ARG SERVER_NAME
ENV SERVER_NAME=${SERVER_NAME:-Tux}
ARG SERVER_EMAIL
ENV SERVER_EMAIL=${SERVER_EMAIL:-git@louvainlinux.org}
ARG GIT_HTTP_BACKEND_PATH
ENV GIT_HTTP_BACKEND_PATH=${GIT_HTTP_BACKEND_PATH:-/usr/lib/git-core/git-http-backend}
ARG GIT_PATH
ENV GIT_PATH=${GIT_PATH:-/data/repos}
ARG KEEP_REPO
ENV KEEP_REPO=${KEEP_REPO}

ENTRYPOINT ["python3", "server.py"]
