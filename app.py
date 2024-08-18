from flask import Flask, request , jsonify


app = Flask(__name__)

@app.route('/ping', methods=['GET'])
def print_health_check():
    return jsonify({"message": "Health Check is working"})

@app.route('/post', methods=['POST'])
def post_test():
    data = request.json
    if "name" in data and data["name"] == "greeting":
        return jsonify({"message": "Greeting received"}), 200
    else:
        return jsonify({"error": "Invalid data"}), 400

if __name__== "__main__":
    app.run(debug=True)
    # app.run(host='0.0.0.0', port=8081)