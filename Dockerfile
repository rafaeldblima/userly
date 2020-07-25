FROM python:3.8-alpine

ENV FLASK_APP api.py
ENV FLASK_CONFIG production
ENV APP_PATH /home/api
ENV PATH $PATH:/root/.local/bin

WORKDIR $APP_PATH

COPY Pipfile Pipfile.lock $APP_PATH/
RUN pip install --upgrade pip && \
    pip install pipenv --user && \
    pipenv run pip install pip && \
    pipenv install --deploy --system && \
    rm -rf /root/.cache

COPY app app
COPY migrations migrations
COPY api.py config.py boot.sh ./
RUN chmod +x ${APP_PATH}/boot.sh

# runtime configuration
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]