FROM python:3.13-slim
# default flask app port.

EXPOSE 5000 
WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt
CMD ["flask", "run", "--host", "0.0.0.0"]