from app.db import engine

try:
    # Try to connect
    conn = engine.connect()
    print("✅ MySQL connection successful!")
    conn.close()
except Exception as e:
    print("❌ MySQL connection failed!")
    print(e)
