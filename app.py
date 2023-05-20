# lt --port 5000
# (Run this line then update request link on code using API to run and access local server)


from flask import Flask, request, jsonify
from flask_cors import CORS

# Initialize a new Flask application
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # This will enable CORS for all routes


# Function to convert kilogram to pounds
def kilo_to_pounds(k):
    p = k * 2.20462
    return round(p)


@app.route("/kilos_to_pounds", methods=["POST"])
def calculate_kilos_to_pounds():
    data = request.get_json()
    # if 'k' not in data:
    #     return jsonify({'error': 'Missing required data'}), 400
    k = data.get("k")
    p = kilo_to_pounds(k)
    return jsonify({"result": p})


# Function to convert pounds to gallons
def pounds_to_gallons(p):
    g = p / 6.7
    return round(g)


@app.route("/pounds_to_gallons", methods=["POST"])
def calculate_pounds_to_gallons():
    data = request.get_json()
    p = data.get("p", 0)
    g = pounds_to_gallons(p)
    return jsonify({"result": g})


# Function to compute needed weight
def needed_weight(req, r, l, c):
    nw = req - r - l - c
    return nw


@app.route("/needed_weight", methods=["POST"])
def calculate_needed_weight():
    data = request.get_json()
    req = data.get("req", 0)
    r = data.get("r", 0)
    l = data.get("l", 0)
    c = data.get("c", 0)
    nw = needed_weight(req, r, l, c)
    return jsonify({"result": nw})


# Function to compute needed gallons
def needed_gallons(nw):
    ng = pounds_to_gallons(nw)
    return ng


# Function to compute total weight
def total_weight(tr, tl, tc):
    t = tr + tl + tc
    return t


@app.route("/total_weight", methods=["POST"])
def calculate_total_weight():
    data = request.get_json()
    # print(data)
    tr = data.get("tr", 0)
    tl = data.get("tl", 0)
    tc = data.get("tc", 0)
    t = total_weight(tr, tl, tc)
    return jsonify({"result": t})


# Function to compute delivered large number
def large_num(a_l_num, b_l_num):
    delivered = a_l_num - b_l_num
    return delivered


# Define the route and allowed methods for the API endpoint
@app.route("/api/solve_equations", methods=["POST"])
def solve_equations():
    # Retrieve data from the request's body
    data = request.get_json()

    # Get individual values from the request's body
    req = data.get("req", 0)
    r = data.get("r", 0)
    l = data.get("l", 0)
    c = data.get("c", 0)
    p = data.get("p", 0)
    a_l_num = data.get("a_l_num", 0)
    b_l_num = data.get("b_l_num", 0)

    # Call the functions and get the results
    g = pounds_to_gallons(p)
    nw = needed_weight(req, r, l, c)
    ng = needed_gallons(nw)
    t = total_weight(r, l, c)
    delivered = large_num(a_l_num, b_l_num)

    # Prepare the response to be sent
    response = {
        "pounds_to_gallons": g,
        "needed_weight": nw,
        "needed_gallons": ng,
        "total_weight": t,
        "delivered": delivered,
    }

    # Convert the Python dictionary into a JSON response
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)
