from flask import Flask, jsonify
import logging

logging.basicConfig(filename="customer-service.log", level=logging.DEBUG)


app = Flask(__name__)


@app.get("/")
def home():
    app.logger.debug("debug log info")
    app.logger.info("Info log information")
    app.logger.warning("Warning log info")
    app.logger.error("Error log info")
    app.logger.critical("Critical log info")
    return {"message": "welcome to customer service"}, 200
