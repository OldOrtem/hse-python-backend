FROM python:3.10 AS base

ARG PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=on \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=500

RUN apt-get update && apt-get install -y gcc
RUN python -m pip install --upgrade pip

WORKDIR /app
COPY ./requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app


FROM base as local
CMD ["uvicorn", "shop_api.main:app", "--host", "0.0.0.0", "--port", "8000"]