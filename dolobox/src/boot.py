# boot.py -- Fichier de configuration exécuté à chaque démarrage

try:
    import main
except ImportError:
    print("main.py not found")

