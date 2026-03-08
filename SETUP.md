# 🏏 World Cup AI Pack — Flask Setup Guide

## Project Structure
```
worldcup-ai-pack/
├── app.py              ← Flask server (main)
├── config.py           ← Config loader
├── requirements.txt    ← Python packages
├── database.sql        ← Supabase table SQL
├── .env.example        ← Environment template
├── templates/
│   ├── index.html      ← Landing page
│   └── success.html    ← After login
└── static/
    └── style.css       ← All styles
```

---

## STEP 1 — Supabase Table

1. https://supabase.com/dashboard/project/ugkornooeeliobnoosta
2. Left sidebar → **SQL Editor** → New Query
3. Paste `database.sql` contents → **Run**

---

## STEP 2 — Google Cloud Console

1. https://console.cloud.google.com → New Project
2. **APIs & Services** → **Credentials**
3. **+ Create Credentials** → **OAuth 2.0 Client ID**
4. Application type: **Web application**
5. Authorized redirect URIs:
   ```
   http://localhost:5000/authorize
   ```
6. Copy **Client ID** and **Client Secret**

---

## STEP 3 — Environment File

```bash
cp .env.example .env
```

Fill `.env`:
```env
DATABASE_URL=postgresql://postgres.ugkornooeeliobnoosta:YOUR_PASS@aws-0-ap-south-1.pooler.supabase.com:6543/postgres
GOOGLE_CLIENT_ID=xxxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-xxxx
SECRET_KEY=any-long-random-string-here
```

---

## STEP 4 — Install & Run

```bash
pip install -r requirements.txt
python app.py
```

Open → http://localhost:5000

---

## User Flow
```
/ (Landing Page)
   ↓ Click "Google se Login"
/login → Google OAuth popup
   ↓ User selects account
/authorize → email extracted
   ↓ INSERT INTO users (email, name)
/success → email shown on screen
```

## Production Deployment (Free)
- **Railway.app** — `pip install -r requirements.txt && python app.py`
- Change redirect URI in Google Console to your Railway URL
