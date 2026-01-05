# Fichier: 3_Simulateurs/capteur.py
import Pyro4
import time
import random

# Connexion au serveur RPC via l'URI définie dans serveur_rpc.py
RPC_URI = "PYRO:safehouse@localhost:9090"

def run_simulation():
    print("📡 Démarrage du simulateur de capteurs (Pyro4)...")
    print(f"   Cible : {RPC_URI}")
    
    # Tentative de connexion
    try:
        # Création du proxy (l'objet distant)
        server = Pyro4.Proxy(RPC_URI)
        
        # Test de connexion simple
        server._pyroBind()
        print("✅ Connecté au serveur RPC avec succès !")
        
    except Exception as e:
        print(f"❌ Impossible de se connecter au serveur RPC : {e}")
        print("   Vérifiez que le Terminal 1 (serveur_rpc.py) est bien lancé.")
        return

    # Boucle infinie d'envoi de données
    while True:
        try:
            # 1. Simuler une température (entre 18.0 et 26.0 degrés)
            temp_actuelle = round(random.uniform(18.0, 26.0), 1)
            
            # 2. Envoyer au serveur RPC
            # La méthode 'update_device' est celle qu'on a créée dans serveur_rpc.py
            server.update_device("temp", temp_actuelle)
            
            print(f"   📤 Envoi température : {temp_actuelle}°C")
            
            # 3. Attendre 5 secondes avant la prochaine mesure
            time.sleep(5)
            
        except Pyro4.errors.ConnectionClosedError:
            print("❌ Connexion perdue avec le serveur RPC. Tentative de reconnexion...")
            time.sleep(5)
        except Exception as e:
            print(f"⚠️ Erreur : {e}")
            time.sleep(5)

if __name__ == "__main__":
    run_simulation()