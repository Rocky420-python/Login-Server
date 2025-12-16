import flask
import bcrypt
from flask import Flask, request, jsonify
from Backend import backend as b
app = Flask(__name__)

@app.route('/')
def home():
    return "Server Working..."

@app.route('/login', methods=["GET"])
def login():
    username = request.args.get("username")
    password = request.args.get("password")

    user1 = b.lg(username, password)
    if user1:
        return jsonify({"message": "Login Successful"}), 200
    else:
        return jsonify({"message": "Login Unsuccessful"}), 200

@app.route('/new_pa', methods=['GET'])
def new_pa():
    username = request.args.get("username")
    password = request.args.get("password")
    user8 = b.save_password(username, password)
    if user8:
        return jsonify({"message": "Username And Password Saved"}), 200
    else:
        return jsonify({"message": "Username And Password Not Saved"}), 401

@app.route("/get_text", methods=["GET"])
def get_text():
    text = request.args.get("text")
    if not text:
        return jsonify({"message": "Text Not Found"}), 404

    # Remove extra quotes if any
    text = text.strip('"')

    # Get response from your backend function
    response = b.get_response(text)

    # Ensure response is JSON serializable
    return jsonify({"response": response}), 200

if __name__ == '__main__':

    app.run(debug=True)
