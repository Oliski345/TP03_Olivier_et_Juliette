# Olivier Pinard (2475333) et Juliette Danis (6302229)
# TP03
import json
import csv




# 1
class AgregateurDonnees:
    def __init__(self):
        # Création liste vide
        self.donnees = []

    def json(self, chemin):
        # Méthode pour fichier json
        try:
            with open(chemin, "w", encoding="utf-8") as f:
                json.dump(chemin, f, indent=4)
            with open(chemin, "r") as f:
                donnee = json.load(f)
                for i in donnee:
                    self.donnees.append({
                        "nom": i["nom"],
                        "prenom": i["prenom"],
                        "age": i["age"],
                        "mathématique": i["notes"]["math"],
                        "science": i["notes"]["science"],
                        "francais": i["notes"]["francais"],
                        "prog": i["notes"]["prog"]
                    })
        except FileNotFoundError:
            print("fichier introuvable")
        except IOError:
            print("Problème accès au fichier jason")
        except Exception as e:
            print(f"Erreur inattendue est survenue:{e}")

    def csv(self, chemin):
        try:
            with open(chemin, "w") as f:
