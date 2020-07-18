FROM python:3.7-alpine

RUN pip install Flask==0.12.2

RUN mkdir /root/code
WORKDIR /root/code
COPY ./knight.py /root/code/main.py

EXPOSE 5000
CMD ["python","/root/code/main.py"]

