import pyodbc

print("--- DIAGNOSTIC SQL SERVER ---")

# 1. Lister les Drivers installés
print("\n1. Pilotes (Drivers) trouvés sur ce PC :")
drivers = [d for d in pyodbc.drivers()]
if not drivers:
    print("   ❌ AUCUN DRIVER ODBC TROUVÉ ! Installez 'ODBC Driver 17 for SQL Server'.")
else:
    for driver in drivers:
        print(f"   - {driver}")

# 2. Test de connexion
# Remplacez ceci par ce que vous pensez être votre serveur
nom_serveur = input("\n2. Entrez le nom du serveur (ex: DESKTOP-XXX\SQLEXPRESS) : ")

drivers_to_test = ['ODBC Driver 17 for SQL Server', 'SQL Server']

print(f"\n3. Tentative de connexion vers : {nom_serveur}...")

reussite = False
for d in drivers_to_test:
    if d in drivers:
        try:
            print(f"   👉 Essai avec le pilote : '{d}' ...")
            conn_str = f'DRIVER={{{d}}};SERVER={nom_serveur};DATABASE=master;Trusted_Connection=yes;'
            conn = pyodbc.connect(conn_str, timeout=5)
            print(f"   ✅ SUCCÈS ! La connexion fonctionne avec ce pilote !")
            print(f"   📝 COPIEZ CETTE LIGNE DANS VOTRE CODE :")
            print(f"      conn = pyodbc.connect('DRIVER={{{d}}};SERVER={nom_serveur};DATABASE=SafeHouseDB;Trusted_Connection=yes;')")
            conn.close()
            reussite = True
            break
        except Exception as e:
            print(f"      ❌ Échec : {e}")

if not reussite:
    print("\n⚠️ CONCLUSION : Impossible de se connecter.")
    print("Causes possibles :")
    print("1. Le nom du serveur est faux. (Vérifiez dans SSMS)")
    print("2. TCP/IP est désactivé (Voir Étape 2 ci-dessous)")