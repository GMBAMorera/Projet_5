# Pur Beurre  
## Contexte  
**Pur Beurre** est une application de suivi des aliments qui va vous permettre de noter quels aliments vous aviez l'habitude de prendre au quotidien et quel aliment vous leur avez préferés.  
  
## Prérequis  
Installer **Pur Beurre** chez vous demande uniquement d'avoir installer Python et sur votre ordinateur.  
Suivez simplement le guide ci-dessous afin de profiter de notre application.  
  
## Installation  
Pour installer **Pur Beurre**, commencez par vous connecter sur [sa page](https://github.com/GMBAMorera/Pur_Beurre).  
Telecharger l'application simplement en cliquant sur le bouton vert à droite de ses fichiers et en choisssant l'option Download ZIP.  
Une fois sur votre disque dur, récupérez le fichier ZIP, posez-le dans le dossier où vous voulez installer **Pur Beurre** et décompressez-le avec l'application de votre choix.  
Entrer dans le dossier Pur_Beurre ainsi créé. Ouvrez-le et copiez son chemin d'accès.
[Installez l'environnement virtuel dans l'invite de commande]  
  
## Utilisation  
Pour utiliser **Pur Beurre**, rien de plus facile!
Ouvrez simplement une invite de commande, par exemple en tapant 'cmd' dans le menu windows, puis basez-la dans le dossier Pur_Beurre en utilisant la commande:  
    cd chemin_d_acces_du_fichier  
Une fois fait, activez l'environnement virtuel avec la commande:
    venv\Scripts\activate  
Puis, tapez la commande:
    python pur_beurre.py  
et laissez_vous guider!  
Suit, plus bas, un descriptif des différentes fonctionnalités de l'application.  
  
### Choix d'un substitut plus sain  
L'application vous demande d'abord de choisir un produit que vous consommez afin de visualiser les substituts recommandés par l'application. Renseignez 1 dans le menu principal afin d'activer cette option.
Pour cela, il vous est d'abord demander de renseigner la catégorie de l'aliment qui vous intéresse, puis de retrouver l'aliment d'origine dans une liste des ingrédients de cette catégorie. N'oubliez pas de renseigner le numéro d'identification de l'aliment, et non son nom.  
Une fois votre aliment choisi, une liste de substituts plus sain vous sera proposé et vous serez libre d'en explorer la composition, en renseignant son identifiant pour le lire en détail et en renseignant 1 ou 2 pour le choisir comme substitut ou bien pour en chercher un autre.  
Une fois votre choix fait, libre à vous de continuer à explorer les substituts, de revenir au menu principal ou de quitter l'application.

### Liste des substituts  
Renseignez 2 dans le menu principal pour accéder à la liste des substituts que vous avez choisis.
Les produits originaux vous sont présentés à gauche et ceux que vous leur avez substitués, à droite.
Lisez la liste à votre guise, puis revenez au menu principal ou quittez l'application.

### Initialisation de la base de données  
Afin de rafraîchir la base de données, vous pouvez décider de la réinitialiser.  
Renseignez Init sur la page d'accueil pour lancer cette fonctionnalité.  
La réinitialisation peut prendre quelques minutes.