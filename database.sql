-- Supabase SQL Editor mein run karo
-- Dashboard → SQL Editor → New Query → Paste → Run

CREATE TABLE IF NOT EXISTS users (
    id         SERIAL PRIMARY KEY,
    email      VARCHAR(200) UNIQUE NOT NULL,
    name       VARCHAR(200),
    picture    TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
