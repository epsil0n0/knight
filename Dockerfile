FROM python:3.7-alpine

RUN pip install Flask gunicorn

RUN mkdir /root/code
COPY ./code /root/code
WORKDIR /root/code

EXPOSE 5000
#CMD ["python","/root/code/main.py"]
CMD gunicorn --bind 0.0.0.0:5000 wsgi:app

