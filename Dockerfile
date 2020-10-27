FROM python:3.6 

RUN apt update
RUN apt install gdal-bin -y

COPY ./app /app
WORKDIR /app
RUN pip install -r requirements.txt

RUN apt install nodejs npm -y
COPY ./frontend /frontend
WORKDIR /frontend
RUN npm install --no-optional
RUN npm run build

CMD ["/app/manage.py","runserver"]
