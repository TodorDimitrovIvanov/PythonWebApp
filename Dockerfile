FROM python:3.7
COPY . /opt/app
WORKDIR /opt/app
RUN pip3 install -r requirements.txt
EXPOSE 3001
CMD ["python3 app.py"]