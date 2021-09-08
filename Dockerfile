FROM python:3.7
RUN pip3 install -r requirements.txt
WORKDIR /code
EXPOSE 3001
COPY . .
CMD ["python3 app.py"]