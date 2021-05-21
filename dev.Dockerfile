FROM python:3-buster AS builder
RUN apt-get update && apt-get upgrade -y &&  apt-get dist-upgrade -y
RUN apt-get install -y --no-install-recommends --yes python3-venv gcc libpython3-dev && \
    python3 -m venv /venv && \
    /venv/bin/pip install --upgrade pip

FROM builder AS builder-venv

COPY requirements.txt /requirements.txt
RUN /venv/bin/pip install -r /requirements.txt

FROM builder-venv AS tester

RUN /venv/bin/pip install pylint flake8 bandit
ENV PATH="/venv/bin:${PATH}"

COPY . /app
WORKDIR /app

ARG ENABLE_BUILD_TEST
ARG ENABLE_BUILD_LINT

RUN if [ "${ENABLE_BUILD_TEST}" != "false" ]; then make test; else echo "Skip test"; fi
RUN if [ "${ENABLE_BUILD_LINT}" != "false" ]; then make lint; else echo "Skip lint"; fi

# FROM martinheinz/python-3.8.1-buster-tools:latest AS runner
FROM python:3-buster AS runner
COPY --from=builder-venv /venv /venv
COPY --from=tester /app /app

RUN mkdir /data

ENV ENABLE_DEBUG_MODE=true
ENV FLASK_ENV=development
WORKDIR /app

ENTRYPOINT ["/venv/bin/python3", "-m", "weasyprint_rest"]
USER 1001

LABEL name={NAME}
LABEL version={VERSION}
