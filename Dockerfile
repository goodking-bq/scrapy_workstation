FROM python:2
WORKDIR /usr/src/app
COPY web_requirements.txt ./
COPY web/ ./web/
COPY run_flask_app.py ./
COPY web_config.py ./
ENV FLASK_APP /usr/src/app/run_flask_app.py
ENV FLASK_DEBUG 0
RUN pip install --no-cache-dir -r web_requirements.txt
RUN rm -rf web/blueprints/home_
MAINTAINER golden
EXPOSE 80
CMD flask run --host=0.0.0.0 --port=80