import os
from flask import Flask, jsonify
from dotenv import load_dotenv

# Load environment variables only when running locally
if os.path.exists("development.env"):
    load_dotenv("development.env")

from livekit.api import AccessToken, VideoGrants

app = Flask(__name__)

def get_env_var(name):
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing environment variable: {name}")
    return value

@app.route("/getToken")
def get_token():
    api_key = get_env_var("LIVEKIT_API_KEY")
    api_secret = get_env_var("LIVEKIT_API_SECRET")

    token = (
        AccessToken(api_key, api_secret)
        .with_identity("identity")
        .with_name("mobile-app")
        .with_grants(VideoGrants(room_join=True, room="my-room"))
        .to_jwt()
    )

    return jsonify({"token": token})

if __name__ == "__main__":
    print("🚀 Flask server started (local mode)")
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),  # Render injecte PORT automatiquement
        debug=False
    )
