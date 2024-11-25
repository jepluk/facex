import sqlite3, time

def open():
    from .cli import DB_NAME
    while True:
        try:
            conn = sqlite3.connect(DB_NAME, timeout=10)  # Timeout 10 detik
            print("[ INFO! ] Open conection.")
            return conn
        except sqlite3.OperationalError as e:
            print(f"[ WARN! ] Connection closed. Opening in 5 minutes! > {e}")
            time.sleep(5)

