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

    def afficher_toutes_solutions(self):
        if self.solutions:
            for i, solution in enumerate(self.solutions):
                print(f"Solution #{i + 1}:")
                for ligne in solution:
                    print(". " * ligne + "Q " + ". " * (self.taille - ligne - 1))
                print()
        else:
            print("Aucune solution disponible.")

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
solveur.afficher_toutes_solutions()
solveur.enregistrer_soluce("solutions_8reines.txt")

#3
"""Fait par juliette"""
class Motdepasse:
    """ Cette classe présente un mot de passe et inclut des méthodes d'analyse"""
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
        """ Vérifie si le mot de passe contient au moins une minuscule"""
        return any(c.islower() for c in self.__valeur)

    def contient_majuscules(self):
        """ Vérifie si le mot de passe contient au moins une majuscule"""
        return any(c.isupper() for c in self.__valeur)

    def contient_chiffres(self):
        """ Vérifie si le mot de passe contient au moins un chiffre"""
        return any(c.isdigit() for c in self.__valeur)

    def contient_symboles(self):
        """ Vérifie si le mot de passe contient au moins un symbole"""
        symboles = "!@#$%^&*()-_+=[]{}|:;',.<>?/"
        return any(c in symboles for c in self.__valeur)

    def calculer_score(self):
        """ Calcule le score de sécurité qu'offre le mot de passe"""
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
        """ Suggère des améliorations possibles d'un mot de passe"""
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

    def tester_force_brute(self, caracteres_connus=0, max_tentatives=10000):
        """ Simule une attaque de force brute sur le mot de passe"""
        debut = time.time()
        charset = string.ascii_letters + string.digits
        mot_de_passe = self.__valeur
        prefix = mot_de_passe[:caracteres_connus]
        pour_briser = mot_de_passe[caracteres_connus:]

        def forcebrute(longueur):
            if longueur == 0:
                return ['']
            plus_petit = forcebrute(longueur - 1)
            return [s + c for s in plus_petit for c in charset]

        essaie = 0
        for x in forcebrute(len(pour_briser)):
            essaie += 1
            if prefix + x == mot_de_passe:
                elapsed = time.time() - debut
                return True, essaie, elapsed
            if essaie >= max_tentatives:
                break

        elapsed = time.time() - debut
        return False, essaie, elapsed

    def estimer_temps_cassage(self):
        """ Estime le temps de cassage du mot de passe"""
        types = 0
        if self.contient_minuscules():
            types += 26
        if self.contient_majuscules():
            types += 26
        if self.contient_chiffres():
            types += 10
        if self.contient_symboles():
            types += 32

        combinaisons = types ** self.__longueur
        temps_secondes = combinaisons / 1_000_000_000

        if temps_secondes < 60:
            return f"{temps_secondes:.2f} secondes"
        elif temps_secondes < 3600:
            return f"{temps_secondes / 60:.2f} minutes"
        elif temps_secondes < 86400:
            return f"{temps_secondes / 3600:.2f} heures"
        elif temps_secondes < 31_536_000:
            return f"{temps_secondes / 86400:.2f} jours"
        else:
            return f"{temps_secondes / 31_536_000:.2f} années"

    def __str__(self):
        """ Donne le mot de passe et son score"""
        masked = self.__valeur[:2] + "*" * (self.__longueur - 2)
        return f"Mot de passe: {masked} (Score: {self.__score_securite}/100)"


class Generateurmotdepasse:
    """ Cette classe génère un mot de passe"""
    def __init__(self):
        self.__minuscules = string.ascii_lowercase
        self.__majuscules = string.ascii_uppercase
        self.__chiffres = string.digits
        self.__symboles = "!@#$%^&*()-_+=[]{}|:;',.<>?/"

    def generer_aleatoire(self, longueur=8, avec_symboles=False):
        """ Génère un mot de passe aléatoire"""
        if longueur < 4:
            raise ValueError("Longueur minimale : 4 caractères")

        pool = [random.choice(self.__minuscules),
                random.choice(self.__majuscules),
                random.choice(self.__chiffres)]
        if avec_symboles:
            pool.append(random.choice(self.__symboles))

        reste = longueur - len(pool)
        caracteres_possibles = self.__minuscules + self.__majuscules + self.__chiffres
        if avec_symboles:
            caracteres_possibles += self.__symboles

        pool += random.choices(caracteres_possibles, k=reste)
        random.shuffle(pool)
        return Motdepasse(''.join(pool))


    def generer_simple(self, mot_base):
        """ Génère un mot de passe simple"""
        substitutions = {'a': '4', 'e': '3', 'i': '1', 'o': '0', 's': '$'}
        mot_modifie = ''.join(substitutions.get(c, c) for c in mot_base.lower())
        mot_modifie += str(random.randint(0, 9))
        return Motdepasse(mot_modifie)


# --- Programme principal ---

# Créer un générateur
generateur = Generateurmotdepasse()

# Générer deux mots de passe
mdp_alea = generateur.generer_aleatoire(longueur=8, avec_symboles=True)
mdp_base = generateur.generer_simple("python")

# Afficher les mots de passe
print("Mots de passe générés :")
print(f"Aléatoire : {mdp_alea.valeur}")
print(f"Basé sur 'python' : {mdp_base.valeur}")

# Analyser les mots de passe
score_alea = mdp_alea.calculer_score()
score_base = mdp_base.calculer_score()
print(f"\nScore du mot de passe aléatoire : {score_alea}/100")
print(f"Score du mot de passe basé sur 'python' : {score_base}/100")

# Obtenir des suggestions d'amélioration
suggestions = mdp_base.suggerer_ameliorations()
print("\nSuggestions d'amélioration pour le mot de passe basé sur 'python' :")
for s in suggestions:
    print(f"- {s}")

# Tester la résistance à la force brute
print("\nTest de force brute (2 premiers caractères connus) :")
resultat, tentatives, temps = mdp_alea.tester_force_brute(caracteres_connus=2, max_tentatives=5000)
if resultat:
    print(f"Mot de passe trouvé en {tentatives} tentatives ({temps:.2f} secondes)")
else:
    print(f"Échec après {tentatives} tentatives ({temps:.2f} secondes)")

# Estimer le temps de cassage
print(f"\nTemps estimé pour casser le mot de passe aléatoire : {mdp_alea.estimer_temps_cassage()}")
print(f"Temps estimé pour casser le mot de passe basé sur 'python' : {mdp_base.estimer_temps_cassage()}")
