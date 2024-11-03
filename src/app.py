from flask import Flask, request, jsonify
import uuid, logging
from src.database import init_db, create, get_customer_by_id, update, delete


logging.basicConfig(filename="customer-service.log", level=logging.DEBUG)

app = Flask(__name__)

# Initialize the database
init_db()


@app.get("/")
def home():
    app.logger.debug("debug log info")
    app.logger.info("Info log information")
    app.logger.warning("Warning log info")
    app.logger.error("Error log info")
    app.logger.critical("Critical log info")
    return {"message": "welcome to customer service"}, 200


@app.post("/customer")
def create_customer():
    request_data = request.get_json()
    new_customer_data = {
        "id": str(uuid.uuid1()),
        "firstname": request_data["firstname"],
        "middlename": request_data.get("middlename", "NA"),
        "lastname": request_data["lastname"],
        "email": request_data["email"],
        "phone": request_data["phone"],
    }
    try:
        new_customer = create(new_customer_data)
        return jsonify(new_customer), 201
    except Exception as e:
        return {"message": str(e)}, 400


@app.get("/customer/<string:id>")
def get_customer(id):
    customer = get_customer_by_id(id)
    if customer:
        return jsonify(customer), 200
    return {"error": "customer id not found"}, 404


@app.put("/customer/<string:id>")
def update_customer(id):
    request_data = request.get_json()
    updated_customer = update(id, request_data)
    if updated_customer:
        return jsonify(updated_customer), 200
    return {"message": "customer not found"}, 404


@app.delete("/customer/<string:id>")
def delete_customer(id):
    if delete(id):
        return {"message": "customer removed successfully"}, 200
    return {"message": "customer not found"}, 404


if __name__ == "__main__":
    app.run(debug=True)
