FROM python:3.10

ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY ./requirements.txt /requirements.txt

RUN pip install --upgrade pip

RUN apt-get update
RUN apt-get -y install libgl1-mesa-glx


RUN pip install -r /requirements.txt

COPY . ./

CMD ["python", "app.py"]