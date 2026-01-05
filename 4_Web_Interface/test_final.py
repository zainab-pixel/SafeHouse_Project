import Pyro4

def test():
    print("⏳ TEST 1: Connexion au serveur RPC...")
    try:
        # On utilise l'adresse EXACTE définie dans votre serveur
        # Si vous avez mis 0.0.0.0, on utilise 127.0.0.1 ici
        server = Pyro4.Proxy("PYRO:safehouse@127.0.0.1:9090")
        
        # On tente une action simple
        server.get_all_states()
        print("✅ RÉSULTAT: SUCCÈS ! Le serveur RPC fonctionne.")
    except Exception as e:
        print(f"❌ RÉSULTAT: ÉCHEC. Le serveur RPC est mort ou bloqué.")
        print(f"   Erreur: {e}")

if __name__ == "__main__":
    test()