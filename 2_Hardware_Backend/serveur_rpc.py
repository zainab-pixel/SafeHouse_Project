print("⏳ Loading libraries...", flush=True)

import Pyro4
import pyodbc
import datetime

# --- CONFIGURATION ---
HOST = "127.0.0.1"
PORT = 9090
OBJ_ID = "safehouse"

# DATABASE DETAILS
DB_SERVER = "localhost"
DB_NAME = "SafeHouseDB"
DRIVER = "{ODBC Driver 17 for SQL Server}"

@Pyro4.expose
class SafeHouseServer(object):
    
    # --- 1. CONNECTION TO SQL SERVER ---
    def get_db_connection(self):
        try:
            conn = pyodbc.connect(
                f'DRIVER={DRIVER};SERVER={DB_SERVER};DATABASE={DB_NAME};Trusted_Connection=yes;'
            )
            return conn
        except Exception as e:
            print(f"❌ DB Error: {e}")
            return None

    # --- 2. USER LOGIN (Check DB + Print) ---
    def login_user(self, email, password):
        print(f"🔑 [LOGIN] Checking user: {email} ... ", end="")
        
        conn = self.get_db_connection()
        if not conn: return {"status": "error", "message": "DB Offline"}

        try:
            cursor = conn.cursor()
            # Check dashboard_appuser table
            cursor.execute("SELECT name, role FROM dashboard_appuser WHERE email = ? AND password = ?", (email, password))
            row = cursor.fetchone()

            if row:
                print("✅ ACCESS GRANTED")
                # Optional: Log the login to history
                self.log_event("Login System", f"User {row[0]} Logged In")
                return {"status": "success", "user": {"name": row[0], "role": row[1]}}
            else:
                print("❌ ACCESS DENIED")
                return {"status": "error", "message": "Invalid Credentials"}
        finally:
            conn.close()

    # --- 3. HARDWARE LOGS (Save + Affiche) ---
    def update_device(self, device_id, value):
        # 1. Prepare Message
        is_on = str(value).lower() == "true"
        state = "ON" if is_on else "OFF"
        icon = "💡"
        
        if "door" in device_id.lower():
            state = "OPEN" if is_on else "CLOSED"
            icon = "🚪"

        # 2. AFFICHE (Print to Console)
        print(f"⚡ [ACTION] {device_id} -> {state} {icon}")

        # 3. SAVE (Insert into dashboard_eventlog)
        self.log_event(device_id, f"Turned {state}")
        
        return {"status": "success", "new_value": value}

    # --- 4. SENSORS (Save + Affiche) ---
    def send_sensor_data(self, sensor_type, value, unit):
        # 1. AFFICHE
        print(f"📡 [SENSOR] {sensor_type}: {value} {unit}")

        # 2. SAVE (Insert into dashboard_sensordata)
        conn = self.get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                query = "INSERT INTO dashboard_sensordata (sensor_type, value, unit, timestamp) VALUES (?, ?, ?, GETDATE())"
                cursor.execute(query, (sensor_type, value, unit))
                conn.commit()
            except Exception as e:
                print(f"   ⚠️ Save Error: {e}")
            finally:
                conn.close()
        
        return {"status": "success"}

    # --- HELPER: Internal Log Saver ---
    def log_event(self, device, action):
        conn = self.get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                query = "INSERT INTO dashboard_eventlog (device_id, action, user_email, timestamp) VALUES (?, ?, 'RPC_Sys', GETDATE())"
                cursor.execute(query, (device, action))
                conn.commit()
            except Exception as e:
                print(f"   ⚠️ Log Error: {e}")
            finally:
                conn.close()

# --- SERVER STARTUP ---
def start_server():
    print(f"⏳ Starting Daemon on {HOST}:{PORT}...")
    try:
        daemon = Pyro4.Daemon(host=HOST, port=PORT)
        uri = daemon.register(SafeHouseServer, OBJ_ID)
        
        print("="*40)
        print(f"🏠 RPC SERVER ONLINE (Database Connected)")
        print(f"🔗 URI: PYRO:{OBJ_ID}@{HOST}:{PORT}")
        print("="*40, flush=True)
        
        daemon.requestLoop()
    except Exception as e:
        print(f"❌ Fatal Error: {e}")

if __name__ == "__main__":
    start_server()