import mysql
from set_database import set_database
from constants import DB_NAME


def main():
    cursor.execute(
        f"USE {DB_NAME}"
    )
    print(
        "Bienvenue dans l'application Pur Beurre!\n"
        "\n"
    )

    a = safety_answers(
        "Que souhaitez-vous faire?\n"
        "1    - Rechercher un substitut à un produit.\n"
        "2    - lire la liste des produits sauvegardés.\n"
        "00   - Quitter le programme.\n"
        "Init - Réinitialiser la base de donnée.\n",
        ["1", "2", "00", "Init"]
    )

    if a == "1":
        search_product()
    elif a == "2":
        saved_list()
    elif a == "Init":
        set_database()


def search_product():
    # Choose between categories
    answers = select(
        "SELECT * FROM categorie",
        "Voici la liste des catégories suivis par notre plateforme:",
        "{} - {}"
    )
    cat = safety_answers(
        "Veuillez indiquer le numéro de la catégorie que vous souhaitez évaluer.\n",
        answers
    )

    # Choose between products
    answers = select(
        f"SELECT id, nom FROM aliment WHERE cat_id={cat}",
        "Voici, pour la catégorie que vous avez choisis,"
        "les aliments qui sont suivis par Pur Beurre.",
        "{} - {}"
    )
    al_id = safety_answers(
        "Veuillez indiquer le numéro de l'aliment que vous souhaitez évaluer.\n",
        answers
    )
    product_view(al_id)


def product_view(al_id):
    cursor.execute(
        "SELECT nom, cat_id, nutriscore, ingredients, saved FROM aliments"
        f"WHERE id = {al_id}"
    )
    for c in cursor:
        aliment, cat_id, nutriscore, ingredients, saved = c
        print(
            f"{aliment} a le nutriscore suivant: {nutriscore}\n"
            "Il est composé de:\n"
            f"{ingredients}\n"
        )
    
    answers = select(
        "SELECT id, nom, nutriscore FROM aliments"
        f"WHERE id!={al_id} AND cat_id={cat_id} AND nutriscore <= {nutriscore}",
        f"\nles produits suivants sont de bons remplaçants pour {aliment}:\n",
        "{} - {} (nutriscore: {})"
    )
    answers += ["S", "MP", "00"]

    #Check if the product is already saved or not
    if saved == 1:
        saving_catchphrase = "Retirer le produit des favoris"
    else:
        saving_catchphrase = "Enregistrer le produit dans les favoris"

    conclusion = safety_answers(
        "Quelle action souhaitez-vous entreprendre?\n"
        "Entrez le numéro du produit de substitution"
        "pour afficher le détail de sa composition.\n"
        "\nOU\n"
        f"\nS - {saving_catchphrase} et revenir au menu principal\n"
        "MP - Revenir au menu principal sans sauvegarder\n"
        "00 - Quitter l'application",
        answers
    )
    if conclusion == "S":
        save_unsave(al_id, saved)
    elif conclusion == "MP":
        main()
    elif conclusion in answers and conclusion != "00":
        product_view(conclusion)

def save_unsave(al_id, saved):
    if saved == 1:
        cursor.execute(f"UPDATE aliments SET saved = 0 WHERE id = {al_id}")
        print("Votre produit a été retiré de la liste des favoris.")
    else:
        cursor.execute(f"UPDATE aliments SET saved = 1 WHERE id = {al_id}")
        print("votre produit a été rajouté à la liste des favoris.")
    main()


def saved_list():
    answers = select(
        "SELECT id, nom FROM aliments WHERE saved = 1",
        "Voici la liste des aliments sauvegardés:",
        "{} - {}"
    )
    answers += ["MP", "00"]
    aliment = safety_answers(
        "Entrez le numéro d'un aliment pour afficher sa liste produit,\n"
        "OU\n"
        "MP - Revenir au menu principal sans sauvegarder\n"
        "00 - Quitter l'application",
        answers
    )

    if type(aliment) is int:
        product_view(aliment)
    elif aliment == "MP":
        main()


def select(instruction, intro, line):
    """ Select data into DB following the given instruction,
    print them and finally ask for the use of it if necessary.
    WARNING: the column order of the query must match exactly
    the order of printing."""
    cursor.execute(instruction)
    answers = []
    print(intro)
    for c in cursor:
        answers.append(str(c[0]))
        print(line.format(*[cc for cc in c]))
    return answers


def safety_answers(question, answers):
    """Ask a question and verify that it is rightly answered."""
    ans = input(question)
    while ans not in answers:
        print("Je suis désolé, je n'ai pas compris votre réponse.")
        ans = input(question)
    return ans


if __name__ == "__main__":
    global cnx, cursor
    cnx = mysql.connector.connect(user='root', password="8&4Douze!")
    cursor = cnx.cursor()

    main()

    cursor.close()
    cnx.close()
