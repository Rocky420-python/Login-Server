import json
import bcrypt
import os
from dotenv import load_dotenv
from openai import OpenAI

# ===================== CONFIG =====================
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
USER_FILE = "RK.json"

# ===================== PASSWORD =====================
def save_password(username, password):
    try:
        hashed_pass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        data = {"username": username, "password": hashed_pass.decode('utf-8')}
        with open(USER_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving password: {e}")
        return False

def lg(username, password):
    try:
        with open(USER_FILE, 'r') as f:
            data = json.load(f)

        hashed = data.get("password", "").encode('utf-8')
        if username == data.get("username") and bcrypt.checkpw(password.encode('utf-8'), hashed):
            return True
        return False
    except Exception as e:
        print(f"Error checking login: {e}")
        return False

# ===================== AI RESPONSE =====================
def get_response(text):
    if not API_KEY:
        print("Error: API_KEY not found in .env")
        return "AI service error"

    try:
        client = OpenAI(api_key=API_KEY, base_url="https://api.groq.com/openai/v1")
        response = client.responses.create(model="openai/gpt-oss-20b", input=text)
        return getattr(response, "output_text", str(response))
    except Exception as e:
        print(f"AI Error: {e}")
        return "AI service error"

g = get_response("hi")
print(g)