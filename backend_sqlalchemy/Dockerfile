FROM python:3.10
ADD . /backend_sqlalchemy
WORKDIR /backend_sqlalchemy
RUN pip install -r requirements.txt
ENTRYPOINT python run.py