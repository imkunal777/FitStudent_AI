"""
setup_and_run.py
----------------
One-click helper script for FitStudent AI.

Usage:
    python setup_and_run.py

What it does:
  1. Reads credentials from .env
  2. Creates the MySQL database (fitstudent_ai) if it doesn't exist
  3. Runs the SQL setup script to create all tables
  4. Starts the Flask development server at http://127.0.0.1:5000
"""

import os
import sys
import subprocess

# ── Load .env ────────────────────────────────────────────────────
from dotenv import load_dotenv
load_dotenv()

HOST   = os.environ.get("MYSQL_HOST",     "localhost")
USER   = os.environ.get("MYSQL_USER",     "root")
PASS   = os.environ.get("MYSQL_PASSWORD", "")
DB     = os.environ.get("MYSQL_DB",       "fitstudent_ai")
PORT   = int(os.environ.get("MYSQL_PORT", 3306))

# ── Step 1: verify PyMySQL can connect ───────────────────────────
print("\n[1/3] Connecting to MySQL ...")
try:
    import pymysql
    conn = pymysql.connect(host=HOST, user=USER, password=PASS,
                           port=PORT, connect_timeout=5)
    print(f"      [OK] Connected to MySQL at {HOST}:{PORT}")
except Exception as e:
    print(f"\n      [ERROR] Cannot connect to MySQL: {e}")
    print("\n  Make sure MySQL is running and your .env password is correct.")
    print("  Edit .env  ->  set MYSQL_PASSWORD=<your root password>")
    sys.exit(1)

# ── Step 2: create database + tables ─────────────────────────────
print("\n[2/3] Creating database and tables ...")
try:
    sql_path = os.path.join("database", "mysql_setup.sql")
    with open(sql_path, "r", encoding="utf-8") as f:
        sql_script = f.read()

    cursor = conn.cursor()

    # Execute each statement in the script
    for statement in sql_script.split(";"):
        stmt = statement.strip()
        if stmt:
            cursor.execute(stmt)

    conn.commit()
    cursor.close()
    conn.close()
    print("      [OK] Database 'fitstudent_ai' and all tables are ready.")
except Exception as e:
    print(f"\n      [ERROR] Database setup error: {e}")
    sys.exit(1)

# ── Step 3: start Flask ───────────────────────────────────────────
print("\n[3/3] Starting FitStudent AI ...")
print("      --> Open your browser at:  http://127.0.0.1:5000")
print("      --> Press Ctrl+C to stop the server.\n")
print("=" * 60)

try:
    subprocess.run([sys.executable, "app.py"], check=True)
except KeyboardInterrupt:
    print("\n\nServer stopped.")
except subprocess.CalledProcessError as e:
    print(f"\nFlask exited with error: {e}")
    sys.exit(1)
