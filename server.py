import os
import subprocess
from flask import Flask, jsonify
from dotenv import load_dotenv
import time

# Load environment variables (for local dev only)
if os.path.exists("development.env"):
    load_dotenv("development.env")

try:
    from livekit.api import AccessToken, VideoGrants
except ImportError:
    raise ImportError("Install livekit-api: pip install livekit-api")

app = Flask(__name__)

def get_env_var(var_name):
    value = os.getenv(var_name)
    if not value:
        raise ValueError(f"Environment variable '{var_name}' is not set.")
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
    )

    return jsonify({"token": token.to_jwt()})


# Optional : launch an extra script if needed
def launch_orion():
    time.sleep(2)
    try:
        script_path = os.path.join(os.path.dirname(__file__), "Launch_Me.py")
        subprocess.Popen(["python", script_path])
        print("🚀 Launch_Me.py started in background.")
    except Exception as e:
        print(f"⚠️ Error running Launch_Me.py: {e}")

if __name__ == "__main__":
    print("⚡ Starting Flask server on Render...")

    # On Render, this is ignored because Gunicorn handles serving,
    # but it remains useful for local testing.
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )
