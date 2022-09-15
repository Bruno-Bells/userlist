FROM python:3.7.11-buster

RUN apt-get update && apt-get install -qq -y \
  build-essential libpq-dev --no-install-recommends \
  && apt-get install -y wget

ENV INSTALL_PATH /project
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install itsdangerous==2.0.0
RUN pip install werkzeug==2.0.3
RUN pip install jinja2==3.0.3


RUN chmod +rwx /etc/ssl/openssl.cnf
RUN sed -i 's/TLSv1.2/TLSv1/g' /etc/ssl/openssl.cnf
RUN sed -i 's/SECLEVEL=2/SECLEVEL=1/g' /etc/ssl/openssl.cnf


COPY . .
RUN pip install --editable .

CMD gunicorn -c "python:config.gunicorn" "project.app:create_app()"
