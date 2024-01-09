FROM nginx:latest

COPY nginx.conf /etc/nginx/nginx.conf
COPY ./app/static /usr/share/nginx/html

EXPOSE 80