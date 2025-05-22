from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/submit-stock', methods=['POST'])
def receive_stock():
    data = request.json
    print("Received stock data:", data)
    url = 'https://script.google.com/macros/s/AKfycbwyP9x-mjl2wu8hYRP0Ctyep2BN4VDLmL9czfR-DoH2gi0JebPG-6M2v2SMuVWE0C_yDw/exec'
    response = requests.post(url, json=data)

    # Print response
    print("Google Status Code:", response.status_code)
    print("Google Response Text:", response.text)
    return jsonify({"message": "Data received!"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
