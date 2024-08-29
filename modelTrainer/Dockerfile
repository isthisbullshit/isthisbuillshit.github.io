FROM pytorch/pytorch

RUN pip install transformers torch accelerate bitsandbytes xgboost scikit-learn
RUN pip install fastapi

WORKDIR /app
COPY src src
COPY entrypoint.sh entrypoint.sh
ARG MODEL_DIR
COPY $MODEL_DIR model

ENTRYPOINT ["/app/entrypoint.sh"]