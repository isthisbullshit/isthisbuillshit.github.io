FROM pytorch/pytorch AS base

WORKDIR /app
COPY requirements/direct.txt requirements/direct.txt

FROM base AS pip_locker
RUN pip freeze | sort > original

RUN pip install -r requirements/direct.txt

RUN pip freeze | sort > new
RUN comm -13 original new > locked_requirements.txt

ENTRYPOINT ["cat", "locked_requirements.txt"]

FROM base AS main

COPY requirements/direct.txt requirements/locked-docker.txt

RUN pip install -r requirements/locked-docker.txt

COPY src src
COPY entrypoint.sh entrypoint.sh
ARG MODEL_DIR
COPY $MODEL_DIR model

ENTRYPOINT ["/app/entrypoint.sh"]
