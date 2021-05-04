### FRONTEND BUILD
FROM node:8.17.0-slim AS nodebuilder 
COPY ./frontend /frontend 
WORKDIR /frontend
RUN npm install --no-optional
RUN npm run build

### APP 
FROM python:3.8
RUN apt update
RUN apt install gdal-bin -y

ENV PRODUCTION=1
COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt

COPY ./app /app
WORKDIR /app
COPY --from=nodebuilder /frontend/dist /app/compiled
RUN ./manage.py collectstatic --noinput

COPY ./cert/ /cert

CMD ["gunicorn","--workers","4","-b","0.0.0.0:80","--forwarded-allow-ips","*","--proxy-allow-from","*","conflictcartographer.wsgi:application"]
