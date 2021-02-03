FROM acait/django-container:1.2.5 as app-container

USER root
RUN apt-get update
RUN apt-get install -y libpq-dev
USER acait

ADD --chown=acait:acait cohort_manager/VERSION /app/cohort_manager/
ADD --chown=acait:acait setup.py /app/
ADD --chown=acait:acait requirements.txt /app/

RUN . /app/bin/activate && pip install -r requirements.txt
RUN . /app/bin/activate && pip install psycopg2

ADD --chown=acait:acait . /app/
ADD --chown=acait:acait docker/app_deploy.sh /scripts/app_deploy.sh
ADD --chown=acait:acait docker/ project/
RUN chmod u+x /scripts/app_deploy.sh
RUN . /app/bin/activate && pip install django-webpack-loader


FROM node:8.15.1-jessie AS wpack
ADD . /app/
WORKDIR /app/
RUN npm install .
RUN npx webpack --mode=production

FROM acait/django-test-container:1.2.5 as app-test-container

COPY --from=app-container /app/ /app/
#COPY --from=app-container /static/ /static/

COPY --chown=acait:acait --from=wpack /app/cohort_manager/static/cohort_manager/bundles/* /app/cohort_manager/static/cohort_manager/bundles/
COPY --chown=acait:acait --from=wpack /app/cohort_manager/static/ /static/
COPY --chown=acait:acait --from=wpack /app/cohort_manager/static/webpack-stats.json /app/cohort_manager/static/webpack-stats.json
