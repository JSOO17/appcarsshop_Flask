FROM python:3.7-alpine
COPY . /web
WORKDIR /web/api
RUN pip install pipenv
RUN pipenv install --system
RUN adduser -D myuser
USER myuser
ENTRYPOINT ["python"]
CMD ["app.py"]