from flask import Flask, redirect, url_for, session, render_template
from authlib.integrations.flask_client import OAuth
import os
import requests
import traceback
from config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY

# ── Google Sheets Webhook URL ──────────────────────────────────
# Render pe SHEETS_WEBHOOK_URL environment variable set karo
SHEETS_WEBHOOK_URL = os.getenv("SHEETS_WEBHOOK_URL", "")

# ── OAuth setup ────────────────────────────────────────────────
oauth = OAuth(app)

google = oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

# ── Google Sheets mein email save karo ────────────────────────
def save_to_sheets(email, name=""):
    try:
        if not SHEETS_WEBHOOK_URL:
            print("[SHEETS] SHEETS_WEBHOOK_URL set nahi hai!")
            return
        response = requests.post(SHEETS_WEBHOOK_URL, json={
            "email": email,
            "name": name
        })
        print(f"[SHEETS] Saved: {email} | Status: {response.status_code}")
    except Exception as e:
        print(f"[SHEETS ERROR] {e}")
        traceback.print_exc()

# ── Routes ─────────────────────────────────────────────────────
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
def login():
    redirect_uri = url_for("authorize", _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route("/authorize")
def authorize():
    try:
        token    = google.authorize_access_token()
        userinfo = token.get('userinfo') or google.userinfo()

        email   = userinfo.get("email", "")
        name    = userinfo.get("name", "")
        picture = userinfo.get("picture", "")

        # Google Sheets mein save karo
        save_to_sheets(email, name)

        session['user'] = {'email': email, 'name': name, 'picture': picture}
        return redirect(url_for("success"))

    except Exception as e:
        print(f"[AUTH ERROR] {e}")
        traceback.print_exc()
        return redirect(url_for("home"))

@app.route("/success")
def success():
    user = session.get('user')
    if not user:
        return redirect(url_for("home"))
    return render_template("success.html", user=user)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

# ── Run ────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)