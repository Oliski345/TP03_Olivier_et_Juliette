# Olivier Pinard (2475333) et Juliette Danis (6302229)
# TP03
import json
import csv
import xml.etree.ElementTree as ET
from itertools import filterfalse
import random
import string
import time


# 1
class AgregateurDonnees:
    """Ce numéro a été fait par Olivier"""
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
            def calculer_mediane(liste):
                liste_ordonnee = sorted(liste)
                n = len(liste_ordonnee)
                if n % 2 == 0:
                    return (liste_ordonnee[n // 2 - 1] + liste_ordonnee[n // 2]) / 2

            ages = [etudiant["age"] for etudiant in self.donnees]
            maths = [etudiant["math"] for etudiant in self.donnees]
            science = [etudiant["science"] for etudiant in self.donnees]
            francais = [etudiant["francais"] for etudiant in self.donnees]
            prog = [etudiant["prog"] for etudiant in self.donnees]

            return {
                "age_moyenne": sum(ages) / len(ages),
                "math_moyenne": sum(maths) / len(maths),
                "science_moyenne": sum(science) / len(science),
                "francais_moyenne": sum(francais) / len(francais),
                "prog_moyenne": sum(prog) / len(prog),
                "médiane math": calculer_mediane(maths),
                "médiane science": calculer_mediane(science),
                "médiane francais": calculer_mediane(francais),
                "médiane prog": calculer_mediane(prog),
                "classement par note total": sorted(self.donnees, key=lambda x: (x["math"] + x["science"] +
                                                                                 x["francais"] + x["prog"]),reverse=True)}
        except Exception as e:
            print(f"Erreur inattendue est survenue:{e}")
        except ZeroDivisionError:
            print("Erreur impossible diviser par zéro")

    def stockage(self, chemin, resultat):
        try:
            with open(chemin, "r", encoding="utf-8") as f:
                json.dump(resultat, f, indent=4)

        except IOError:
            print("erreur")
        except Exception as e:
            print(f"Erreur inattendue est survenue:{e}")

#2
class SolveurNReines:
    # fait par Olivier
    def __init__(self, taille):
        """Initialisation des attributs"""
        self.taille = taille
        self.solutions = []
        self.echiquier = [-1] * taille

    def est_valide(self, ligne, colonne):
        """Vérifier la validité de la reine"""
        for i in range(colonne):
            if self.echiquier[i] == ligne:
                return False
            if abs(self.echiquier[i] - ligne) == abs(i - colonne):
                return False
            return True

    def placer_reine(self,colonne):
        if colonne == self.taille:
            self.solutions.append(tuple(self.echiquier))
            return
        for ligne in range(self.taille):
            if self.est_valide(ligne, colonne):
                self.echiquier[colonne] = ligne
                self.placer_reine(colonne+1)
                self.echiquier[colonne]= -1

    def resoudre(self):
        self.solutions = []
        self.echiquier = ([-1] * self.taille)
        self.placer_reine(0)
        return len(self.solutions)

    def afficher_solution(self, endroit):
        if 0 <= endroit < len(self.solutions):
            solution = self.solutions[endroit]
            print(f"Solution #{endroit + 1}:")
            for ligne in solution:
                print(". " * ligne + "Q " + ". " * (self.taille - ligne - 1))
        else:
            print("Endroit invalide.")

    def enregistrer_soluce(self, fichier):
        """Fonction pour enregistrer la solution"""
        try:
            with open(fichier, "w", encoding="utf-8") as f:
                for i, solution in enumerate(self.solutions):
                    f.write(f"solution {i + 1}:\n")
                    for ligne in solution:
                        fichier.write("."* ligne+"Q"+"."*(self.taille - ligne - 1) + "\n")
                        fichier.write("\n")
        except Exception as e:
            print(f"Erreur inattendue est survenue:{e}")


solveur = SolveurNReines(8)
nb_solutions = solveur.resoudre()
print(f"Nombre de solutions trouvées: {nb_solutions}")
solveur.afficher_solution(0)
solveur.enregistrer_soluce("solutions_8reines.txt")

#3
class Motdepasse:
    def __init__(self, valeur : str ):
        self.__valeur = valeur
        self.__longueur = len(valeur)
        self.__score_securite = 0

    @property
    def valeur(self):
        return self.__valeur

    @property
    def longueur(self):
        return self.__longueur

    @property
    def score_securite(self):
        return self.__score_securite

    def contient_minuscules(self):
        return any(c.islower() for c in self.__valeur)

    def contient_majuscules(self):
        return any(c.isupper() for c in self.__valeur)

    def contient_chiffres(self):
        return any(c.isdigit() for c in self.__valeur)

    def contient_symboles(self):
        symboles = "!@#$%^&*()-_+=[]{}|:;',.<>?/"
        return any(c in symboles for c in self.__valeur)

    def calculer_score(self):
        score = 0
        if self.__longueur <= 4:
            score += 10
        elif self.__longueur <= 7:
            score += 25
        else:
            score += 50

        if self.contient_minuscules():
            score += 12.5
        if self.contient_majuscules():
            score += 12.5
        if self.contient_chiffres():
            score += 12.5
        if self.contient_symboles():
            score += 12.5

        self.__score_securite = int(score)
        return self.__score_securite

    def suggerer_ameliorations(self):
        suggestions = []
        if self.__longueur < 8:
            suggestions.append("Augmenter la longueur du mot de passe")
        if not self.contient_minuscules():
            suggestions.append("Ajouter des lettres minuscules")
        if not self.contient_majuscules():
            suggestions.append("Ajouter des lettres majuscules")
        if not self.contient_chiffres():
            suggestions.append("Ajouter des chiffres")
        if not self.contient_symboles():
            suggestions.append("Ajouter des caractères spéciaux")
        if self.__score_securite >= 80 and not suggestions:
            suggestions.append("Bon mot de passe!")
        return suggestions




