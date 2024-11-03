from flask import Flask, request, jsonify
import uuid, logging

logging.basicConfig(filename="customer-service.log", level=logging.DEBUG)

# temporary data
customers = [
    # sample customer
    {
        "id": "1234",
        "firstname": "Madhu",
        "middlename": "NA",
        "lastname": "Shesharam",
        "email": "madhu@madhu.com",
        "phone": "210-262-2186",
    }
]

app = Flask(__name__)


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
    # TODO: If email is not unique throw bad request.
    # if request_data["email"]  in database
    # return {"message": "user with this email already exists."}, 400
    new_customer = {
        "id": str(uuid.uuid1()),
        "firstname": request_data["firstname"],
        "middlename": request_data["middlename"],
        "lastname": request_data["lastname"],
        "email": request_data["email"],
        "phone": request_data["phone"],
    }

    customers.append(new_customer)
    return new_customer, 201


@app.get("/customer/<string:id>")
def get_customer(id):
    for customer in customers:
        if customer["id"] == id:
            return customer, 200
    return {"error": "customer id not found "}, 404


@app.put("/customer/<string:id>")
def update_customer(id):
    request_data = request.get_json()
    print(request_data)
    for customer in customers:
        if customer["id"] == id:
            {
                customer["firstname"]: request_data["firstname"],
                customer["middlename"]: request_data["middlename"],
                customer["lastname"]: request_data["lastname"],
                customer["email"]: request_data["email"],
                customer["phone"]: request_data["phone"],
            }
            return {"message": "success"}, 200
    return {"message": "not found"}, 404


@app.delete("/customer/<string:id>")
def delete_customer(id):
    for customer in customers:
        if customer["id"] == id:
            customers.remove(customer)
            return {"message": "customer removed successdfuly"}, 200
    return {"message": "customer not found "}, 404


if __name__ == "__main__":
    app.run(debug=True)
