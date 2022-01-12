ARG PY_IMAGE_VARIANT=slim
ARG PYTHON_VERSION=3.9.5

FROM python:${PYTHON_VERSION}-${PY_IMAGE_VARIANT} AS compile-image

RUN apt-get update && \
    python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY ./requirements.txt ${CONTAINER_BASE_DIR}/requirements.txt

COPY ./requirements.txt /requirements.txt

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /requirements.txt


FROM python:${PYTHON_VERSION}-${PY_IMAGE_VARIANT} AS build-image

LABEL name="InfluxDB-demo" \
      license="MIT License"

COPY --from=compile-image /opt/venv /opt/venv

ENV PATH=/opt/venv/bin:$PATH \
    PYTHONPATH=/opt/venv/bin:$PYTHONPATH \
    PYTHONUNBUFFERED=1

COPY ./src /app/
WORKDIR /app

ENTRYPOINT ["python", "-u", "main.py"]