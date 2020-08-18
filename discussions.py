"""Contain, for all files, print discussion
with the user of Pur Beurre.
"""

### MAIN ###
WELCOME = (
    "\n\n"
    "Bienvenue dans l'application Pur Beurre!\n"
    "\n"
)

GOODBYE = (
    "Merci d'avoir choisi Pur Beurre"
    " dans votre lutte pour une alimentation plus saine!\n"
    "Nous espérons vous revoir bientôt."
)

CATEGORIES_PRESENTATION = (
    "Voici la liste des catégories"
    " suivies par notre plateforme:"
)
SELECT_CAT = (
    "Veuillez indiquer le numéro de la"
    " catégorie que vous souhaitez évaluer.\n"
)

AL_PRESENTATION = (
    "Voici, pour la catégorie que vous avez choisie,"
    " les aliments qui sont suivis par Pur Beurre."
)
SELECT_AL = (
    "Veuillez indiquer le numéro de l'aliment"
    " que vous souhaitez évaluer.\n"
)
PRESENT_SUBST = (
    "\nles produits suivants sont de bons substituts pour {}:\n"
)

SUBST_PRESENTATION = (
    "Voici, pour chaque produit, le produit"
    " de substitution que vous avez sauvegardé:\n"
)

M_1 = "1"
M_2 = "2"
MP = "MP"
Q = "00"
I = "Init"

MAIN_MENU = (
    "Que souhaitez-vous faire?\n"
    f"{M_1} - Rechercher un substitut à un produit.\n"
    f"{M_2} - lire la liste des substituts.\n"
    f"{Q} - Quitter le programme.\n"
    f"{I} - Initialiser ou Réinitialiser la base de donnée.\n"
)

SUBST_MENU = (
    "\nQuelle action souhaitez-vous entreprendre?\n"
    "Entrez le numéro d'un produit alternatif "
    "pour afficher le détail de sa composition.\n"
    "OU\n"
    f"{MP} - Revenir au menu principal.\n"
    f"{Q} - Quitter l'application.\n"
)

SAVE_MENU  =(
    "\n\n"
    "Voulez-vous:\n"
    f"{M_1} - Choisir ce produit comme substitut.\n"
    "OU\n"
    f"{M_2} - Revenir au choix de substituts.\n"
    f"{MP} - Revenir au menu principal.\n"
    f"{Q} - Quitter l'application.\n"
)

MAIN_OR_QUIT = (
    "Que souhaitez-vous faire?\n"
    f"{MP} - Menu Principal\n"
    f"{Q} - Quitter le programme.\n"
)

SAVE_ANSWERS = [M_1, M_2, MP, Q]
MAIN_ANSWERS = [M_1, M_2, Q, I]
BACK_ANSWERS = [MP, Q]

ID_NAME_FORMAT = "{} - {}"
ID_NAME_NUTR_FORMAT = "{} - {} (nutriscore: {})"

NOT_AN_ANSWER = "Je suis désolé, je n'ai pas compris votre réponse."



### DATABASE.PY ###
PRODUCT_VIEW = (
    "\n\n"
    "{} a le nutriscore suivant: {}\n"
    "Il est composé de:\n"
    "{}\n"
)
VALID_SUBST = (
    "{} a bien été enregistré comme le produit de substition de {}"
)
SEPARATOR = "\n\n-------------------------------------------"
SUBST_FORMAT = "{}: {}"



### INITDATABASE ###
INIT_DB = "loading database..."
SUCCESS_INIT_DB = "Database successfully initialized."
FAIL_INIT_DB = "failed to load database, erasing..."
ERASE_DB = "database erased"

CREATE_TB = "Creating table {}"
CREATE_TB_SUCCESS = "{} table augmented"

CAT_FINDING = 'Beginning to find products for category {}'
CAT_FINDING_FAIL = "not enough product in the category {}"
CAT_FINDING_SUCCESS = (
    "after seeing {} page of products, the category {} is filled"
)



