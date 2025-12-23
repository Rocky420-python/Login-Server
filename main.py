import re
from flask import Flask, jsonify, request
import json
import pandas as pd


from openai import OpenAI


app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message" : "Hello Admin"})

@app.route('/login', methods=["GET"])
def login():
    username = request.args.get("username")
    password = request.args.get("password")
    
    if not username:
        return jsonify({"message" : "Please enter your username."})

    if not password:
        return jsonify({"message": "Please enter your password."})

    # Validate username length: should be between 7 and 8 characters inclusive
    if len(username) < 7 or len(username) > 8:
        return jsonify({"message" : "Username must be between 7 and 8 characters long."})

    # Validate password length: should be between 8 and 9 characters inclusive
    if len(password) < 8 or len(password) > 9:
        return jsonify({"message" : "Password must be between 8 and 9 characters long."})

    try:
        with open("RK.json", "r") as f:
            data = json.load(f)

        # data is expected to be a list of user dictionaries
        user_found = any(user['username'] == username and user['password'] == password for user in data)

        if user_found:
            return jsonify({"message": "Login Successful"})
        else:
            return jsonify({"message": "Invalid Username or Password."})
    except Exception as e:
        return jsonify({"message": f"Error: {e}"})


@app.route('/register', methods=["GET"])
def register():
    username = request.args.get("username")
    password = request.args.get("password")
    email = request.args.get("email")

    if not username:
        return jsonify({"message": "Please enter your username."})
    if not password:
        return jsonify({"message": "Please enter your Password."})
    if not email:
        return jsonify({"message": "Please enter your email."})

    if len(username) < 7 or len(username) > 8:
        return jsonify({"message": "Username must be between 7 and 8 characters long."})

    if len(password) < 8 or len(password) > 9:
        return jsonify({"message": "Password must be between 8 and 9 characters long."})

    try:
        with open("RK.json", "r") as f:
            users = json.load(f)
    except FileNotFoundError:
        users = []

    # চেক করুন ইউজার পূর্বে রয়েছে কিনা
    if any(user["username"] == username for user in users):
        return jsonify({"message": "Username Already Registered"})

    new_user = {
        "username": username,
        "password": password,
        "email": email
    }

    users.append(new_user)

    try:
        with open("RK.json", "w") as f:
            json.dump(users, f, indent=4)
        return jsonify({"message": "Register Success"})
    except Exception as e:
        return jsonify({"message": f"Error: {e}"})


@app.route('/new_api', methods=["GET"])
def new_api():
    api = request.args.get("api")
    if not api:
        return jsonify({"message": "Please enter your api."})

    # Create a DataFrame with a single record
    data = {"api": [api]}
    df = pd.DataFrame(data)

    try:
        # Convert DataFrame to JSON string with indentation
        json_str = df.to_json(orient='records', indent=4)
        # Write the JSON string to file
        with open("Htt.json", "w") as f:
            f.write(json_str)
        return jsonify({"message": "Api Set Successful"})
    except Exception as e:
        return jsonify({"message": f"Error: {e}"})

@app.route('/get_response', methods=["GET"])
def get_response():
    text = request.args.get("text")
    if not text:
        return jsonify({"message" : "Please enter your message."})

    try:
        with open("Htt.json", "r") as f:
            json_data = json.load(f)
        # json_data is a list of dicts, e.g., [{"api": "your_api"}]
        if json_data:
            api_value = json_data[0].get("api")

            client = OpenAI(
             api_key=api_value,
             base_url="https://api.groq.com/openai/v1"
             )
            response = client.responses.create(
            model="openai/gpt-oss-20b",
            input=text
                )

            res = response.output_text
            res = res.replace("ChatGPT", "Rocky ☠")
            res = res.replace("OpenAI", "RK Rocky 👻")


            return jsonify({'message' : res})
        else:
            return jsonify({"message": "No API found."})
    except FileNotFoundError:
        return jsonify({"message": "API file not found."})
    except Exception as e:
        return jsonify({"message": f"Error: {e}"})


@app.route('/fix_code', methods=["GET"])
def fix_code():
    code = request.args.get("code")
    if not code:
        return jsonify({"message" : "Please enter your code."})

    try:
        with open("Htt.json", "r") as f:
            json_data = json.load(f)
        # json_data is a list of dicts, e.g., [{"api": "your_api"}]
        if json_data:
            api_value = json_data[0].get("api")

            text = f"Hi Im a Developer But My Code Is Error, They code is {code}, your just fix it and add fix comment in bangla + english, just fix nothing say anything else. "
            client = OpenAI(
             api_key=api_value,
             base_url="https://api.groq.com/openai/v1"
             )
            response = client.responses.create(
            model="openai/gpt-oss-20b",
            input=text
                )

            res = response.output_text
            res = res.replace("ChatGPT", "Rocky ☠")
            res = res.replace("OpenAI", "RK Rocky 👻")


            return jsonify({'message' : res})
        else:
            return jsonify({"message": "No API found."})
    except FileNotFoundError:
        return jsonify({"message": "API file not found."})
    except Exception as e:
        return jsonify({"message": f"Error: {e}"})


if __name__ == "__main__":
    app.run(debug=True)

