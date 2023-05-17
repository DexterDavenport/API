from flask import Flask, request, jsonify
from flask_cors import CORS

# Initialize a new Flask application
app = Flask(__name__)
CORS(app) # This will enable CORS for all routes

# Function to convert kilogram to pounds
def kilo_to_pounds(k):
    p = k * 2.20462
    return p

# Function to convert pounds to gallons
def pounds_to_gallons(p):
    g = p / 6.7
    return g

# Function to compute needed weight
def needed_weight(req, r, l, c):
    nw = req - r - l - c
    return nw

@app.route('/needed_weight', methods=['POST'])
def calculate_needed_weight():
    data = request.get_json()
    req = data.get('req', 0)
    r = data.get('r', 0)
    l = data.get('l', 0)
    c = data.get('c', 0)
    nw = needed_weight(req, r, l, c)
    return jsonify({'result': nw})

# Function to compute needed gallons
def needed_gallons(nw):
    ng = pounds_to_gallons(nw)
    return ng

# Function to compute total weight
def total_weight(r, l, c):
    t = r + l + c
    return t

# Function to compute delivered large number
def large_num(a_l_num, b_l_num):
    delivered = a_l_num - b_l_num
    return delivered

# Define the route and allowed methods for the API endpoint
@app.route('/api/solve_equations', methods=['POST'])
def solve_equations():
    # Retrieve data from the request's body
    data = request.get_json()

    # Get individual values from the request's body
    req = data.get('req', 0)
    r = data.get('r', 0)
    l = data.get('l', 0)
    c = data.get('c', 0)
    a_l_num = data.get('a_l_num', 0)
    b_l_num = data.get('b_l_num', 0)

    # Call the functions and get the results
    nw = needed_weight(req, r, l, c)
    ng = needed_gallons(nw)
    t = total_weight(r, l, c)
    delivered = large_num(a_l_num, b_l_num)

    # Prepare the response to be sent
    response = {
        'needed_weight': nw,
        'needed_gallons': ng,
        'total_weight': t,
        'delivered': delivered
    }

    # Convert the Python dictionary into a JSON response
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
