FROM python:3-buster AS builder
RUN apt-get update && apt-get upgrade -y &&  apt-get dist-upgrade -y
RUN apt-get install -y --no-install-recommends --yes python3-venv gcc libpython3-dev && \
    python3 -m venv /venv && \
    /venv/bin/pip install --upgrade pip

COPY requirements.txt /requirements.txt
RUN /venv/bin/pip install -r /requirements.txt

RUN /venv/bin/pip install pylint flake8 bandit
ENV PATH="/venv/bin:${PATH}"

COPY . /app
WORKDIR /app

ARG ENABLE_BUILD_TEST_IMAGE_UPDATE
ENV ENABLE_BUILD_TEST_IMAGE_UPDATE=${ENABLE_BUILD_TEST_IMAGE_UPDATE}
ARG ENABLE_BUILD_TEST
ARG ENABLE_BUILD_LINT

RUN if [ "${ENABLE_BUILD_TEST}" != "false" ] && [ "${ENABLE_BUILD_TEST_IMAGE_UPDATE}" != "true" ]; then make test; else echo "Skip test"; fi
RUN if [ "${ENABLE_BUILD_LINT}" != "false" ]; then make lint; else echo "Skip lint"; fi

RUN mkdir /data

ENV ENABLE_DEBUG_MODE=true
ENV FLASK_ENV=development
ENV PATH="/venv/bin:${PATH}"

WORKDIR /app
ENTRYPOINT ["/app/run-dev.sh"]
#USER 1001

LABEL name={NAME}
LABEL version={VERSION}
