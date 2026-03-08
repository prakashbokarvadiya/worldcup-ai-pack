from flask import Flask, redirect, url_for, session, render_template, request
from authlib.integrations.flask_client import OAuth
import psycopg2
import os
from config import DATABASE_URL, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY

# ── OAuth setup ────────────────────────────────────────────────
oauth = OAuth(app)

google = oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

# ── Database ───────────────────────────────────────────────────
def get_conn():
    return psycopg2.connect(DATABASE_URL, sslmode='require')

def save_user(email, name=None, picture=None):
    conn = get_conn()
    cur  = conn.cursor()
    cur.execute(
        """INSERT INTO users (email, name, picture)
           VALUES (%s, %s, %s)
           ON CONFLICT (email) DO UPDATE SET
               name    = EXCLUDED.name,
               picture = EXCLUDED.picture""",
        (email, name, picture)
    )
    conn.commit()
    cur.close()
    conn.close()

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
    token    = google.authorize_access_token()
    userinfo = token.get('userinfo') or google.userinfo()

    email   = userinfo.get("email")
    name    = userinfo.get("name", "")
    picture = userinfo.get("picture", "")

    save_user(email, name, picture)

    session['user'] = {'email': email, 'name': name, 'picture': picture}

    return redirect(url_for("success"))

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
