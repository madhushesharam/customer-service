FROM python:3.13-slim
# default flask app port.

EXPOSE 5000 
WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

# CMD ["flask", "run", "--host", "0.0.0.0"]


# Enable OpenTelemetry logging auto-instrumentation and Run Flask with OpenTelemetry instrumentation
ENV OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
CMD ["sh", "-c", "opentelemetry-instrument --traces_exporter console --metrics_exporter console --logs_exporter console --service_name dice-server flask run --host 0.0.0.0 -p 5000"]