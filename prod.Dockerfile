FROM python:slim-buster AS builder
RUN apt-get update && \
    apt-get install --no-install-suggests --no-install-recommends --yes python3-venv gcc libpython3-dev gtk+3.0 && \
    python3 -m venv /venv && \
    /venv/bin/pip install --upgrade pip

FROM builder AS builder-venv
COPY requirements.txt /requirements.txt
RUN /venv/bin/pip install --disable-pip-version-check -r /requirements.txt

FROM builder-venv AS tester
COPY . /app
WORKDIR /app
RUN /venv/bin/pytest

FROM python:slim-buster AS runner
RUN apt-get update && \
    apt-get install --no-install-suggests --no-install-recommends --yes gtk+3.0 curl jq

COPY --from=tester /venv /venv
COPY --from=tester /app/weasyprint_rest /app/weasyprint_rest
ENV PRODUCTION "true"
ENV FLASK_ENV=production

WORKDIR /app
ENTRYPOINT ["/venv/bin/waitress-serve", "--port=5000", "--host=0.0.0.0", "--call" ,"weasyprint_rest:create_app"]

HEALTHCHECK --start-period=5s --interval=10s --timeout=10s --retries=5 \
    CMD curl --silent --fail --request GET http://localhost:5000/api/v1.0/health \
        | jq --exit-status '.status == "OK"' || exit 1

USER 1001
LABEL name={NAME}
LABEL version={VERSION}
