FROM python:3.7
WORKDIR /code
RUN pip3 install -r requirements.txt
EXPOSE 3001
COPY . .
CMD ["python3 app.py"]