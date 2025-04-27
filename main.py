# Olivier Pinard (2475333) et Juliette Danis (6302229)
# TP03
import json
import csv
import xml.etree.ElementTree as ET



# 1
class AgregateurDonnees:
    def __init__(self):
        # Création liste vide
        self.donnees = []

    def lire_json(self, chemin):
        # Méthode pour fichier json
        try:
            with open(chemin, "w", encoding="utf-8") as f:
                json.dump(chemin, f, indent=4)
            with open(chemin, "r", encoding="utf-8") as f:
                donnee = json.load(f)
                for i in donnee:
                    self.donnees.append({
                        "nom": i["nom"],
                        "prenom": i["prenom"],
                        "age": i["age"],
                        "math": i["notes"]["math"],
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

    def lire_csv(self, chemin):
        """Méthode pour fichier csv"""
        try:
            with open(chemin, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for ligne in reader:
                    self.donnees.append({
                        "nom": ligne["nom"],
                        "prenom": ligne["prenom"],
                        "age": ligne["age"],
                        "math": ligne["math"],
                        "science": ligne["science"],
                        "francais": ligne["francais"],
                        "prog": ligne["prog"]
                    })
        except FileNotFoundError:
            print("fichier introuvable")
        except ValueError:
            print("Erreur les données ne sont pas valables")
        except Exception as e:
            print(f"Erreur inattendue est survenue:{e}")

    def lire_xml(self, chemin):
        """Méthode pour fichier xml"""
        try:
            arbre = ET.parse(chemin)
            racine = arbre.getroot()
            for etudiant in racine.findall("etudiant"):
                self.donnees.append({
                    "nom": etudiant.find("nom").text,
                    "prenom": etudiant.find("prenom").text,
                    "age": int(etudiant.find("age").text),
                    "math": float(etudiant.find("math").text),
                    "science": float(etudiant.find("science").text),
                    "francais": float(etudiant.find("francais").text),
                    "prog": float(etudiant.find("prog").text)
                })
        except FileNotFoundError:
            print("fichier introuvable")
        except ValueError:
            print("Erreur les données ne sont pas valables")
        except Exception as e:
            print(f"Erreur inattendue est survenue:{e}")

    def calculer_statistique(self):
        try:
            ages = [etudiant["age"] for etudiant in self.donnees]
            maths = [etudiant["math"] for etudiant in self.donnees]
            science = [etudiant["science"] for etudiant in self.donnees]
            francais = [etudiant["francais"] for etudiant in self.donnees]
            prog = [etudiant["prog"] for etudiant in self.donnees]

            return
