import psycopg2

try:
    print("🔄 Database se connect kar raha hoon...")

    conn = psycopg2.connect(
        "postgresql://postgres:qwsaxzqwsax@db.ugkornooeeliobnoosta.supabase.co:5432/postgres"
    )

    print("✅ Database connected successfully!")

    conn.close()

except Exception as e:
    print("❌ Connection failed!")
    print("Error:", e)