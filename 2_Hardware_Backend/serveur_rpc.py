# Fichier: 2_Hardware_Backend/serveur_rpc.py
import Pyro4
import pyodbc
import datetime

# --- CONFIGURATION SQL SERVER (Authentification Windows) ---
CONN_STR = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=SafeHouseDB;"
    "Trusted_Connection=yes;"
)

@Pyro4.expose # Rend la classe accessible au réseau
class SafeHouseServer:
    def __init__(self):
        print("✅ Serveur RPC Démarré et prêt.")
        # État initial (Mémoire RAM)
        self.state = {
            # Lumières
            "living-light": False,
            "kitchen-light": False,
            "garden-light": False,
            
            # Climat
            "temp": 21,
            "eco-mode": True,
            
            # Sécurité
            "alarm": True,
            "camera": True,
            "notification": False,
            
            # Garage
            "garage-door": False, 
            "garage-light": False,
            
            # Energie
            "energy-meter": 42,
            "energy-eco": True,
            "ev-charge": False,
            
            # Arrosage
            "watering-main": False,
            "soil-threshold": 35
        }

    def get_all_states(self):
        """Appelé par Django au chargement de la page pour tout afficher"""
        print(f"[LECTURE] Django demande l'état complet.")
        return self.state

    def update_device(self, device_id, value):
        """Appelé par Django quand on clique sur un bouton"""
        print(f"[ACTION] Demande reçue : {device_id} -> {value}")
        
        # 1. Mise à jour de la mémoire
        if device_id in self.state:
            self.state[device_id] = value
        else:
            print(f"⚠️ Attention : ID inconnu '{device_id}' ajouté à l'état.")
            self.state[device_id] = value

        # 2. Sauvegarde dans SQL Server (Historique capteurs)
        self._save_to_db(device_id, value)
        
        # 3. Sauvegarde dans SQL Server (Journal des Logs)
        description = f"L'utilisateur a changé {device_id} vers {value}"
        self._log_event("ACTION_UTILISATEUR", description)
        
        return True

    def _save_to_db(self, device_id, value):
        """Méthode privée pour écrire dans SensorData"""
        try:
            conn = pyodbc.connect(CONN_STR)
            cursor = conn.cursor()
            
            val_float = None
            val_string = None
            
            if isinstance(value, bool):
                val_string = "ON" if value else "OFF"
            elif isinstance(value, (int, float)):
                val_float = float(value)
            else:
                val_string = str(value)

            sql = """
                INSERT INTO SensorData (sensor_type, value_float, value_string, zone)
                VALUES (?, ?, ?, ?)
            """
            cursor.execute(sql, (device_id, val_float, val_string, 'maison'))
            conn.commit()
            cursor.close()
            conn.close()
            print(f"   └── 💾 Donnée sauvegardée.")
        except Exception as e:
            print(f"   ❌ Erreur SQL (SensorData) : {e}")

    def _log_event(self, event_type, description):
        """Méthode privée pour écrire dans EventLogs"""
        try:
            conn = pyodbc.connect(CONN_STR)
            cursor = conn.cursor()
            sql = "INSERT INTO EventLogs (event_type, description) VALUES (?, ?)"
            cursor.execute(sql, (event_type, description))
            conn.commit()
            cursor.close()
            conn.close()
            print(f"   └── 📝 Log ajouté : {description}")
        except Exception as e:
            print(f"   ❌ Erreur SQL (EventLogs) : {e}")

# --- LANCEMENT DU SERVEUR PYRO4 ---
def start_server():
    daemon = Pyro4.Daemon(port=8000)
    uri = daemon.register(SafeHouseServer, "safehouse")
    
    print(f"🔥 Serveur Pyro4 en écoute sur : {uri}")
    print("   (Laissez cette fenêtre ouverte !)")
    
    daemon.requestLoop()

if __name__ == "__main__":
    start_server()