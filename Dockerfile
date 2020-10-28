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

COPY ./app /app
WORKDIR /app
RUN pip install -r requirements.txt
COPY --from=nodebuilder /frontend/dist /app/static

CMD ["/app/manage.py","runserver"]
