FROM python:3

WORKDIR /flask-docker

RUN python3 -m pip install --upgrade pip

COPY requirements.txt requirements.txt
COPY database.db database.db

RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3" ,"-m" , "flask", "run", "--host=0.0.0.0" ]