import os
import mysql
from Database import Database

from constants import DB_NAME

class Engine:
    """ Main class, running the Pur Beurre application."""


    def __init__(self):
        self.db = Database()


    def main(self):
        os.system('cls')
        
        print(
            "\n\n"
            "Bienvenue dans l'application Pur Beurre!\n"
            "\n"
        )
        a = self._safety_answers(
            "Que souhaitez-vous faire?\n"
            "1    - Rechercher un substitut à un produit.\n"
            "2    - lire la liste des substituts.\n"
            "00   - Quitter le programme.\n"
            "Init - Initialiser ou Réinitialiser la base de donnée.\n",
            ["1", "2", "00", "Init"]
        )

        if a == "1":
            self._search_prod()
        elif a == "2":
            self._show_subst()
        elif a == "00":
            self._quit()
        elif a == "Init":
            self.db.initialize()
            self.main()


    def _search_prod(self):
        os.system('cls')
        
        # Choose between categories
        categories = self.db.load_table(
            "categories",
            "",
            "Voici la liste des catégories suivis par notre plateforme:",
            "{} - {}"
        )

        cat_id = self._safety_answers(
            "Veuillez indiquer le numéro de la catégorie que vous souhaitez évaluer.\n",
            [cat[0] for cat in categories.array]
        )

        # Choose between products
        products = self.db.load_table(
            "aliments",
            f"WHERE cat_id={cat_id}",
            "Voici, pour la catégorie que vous avez choisis,"
            "les aliments qui sont suivis par Pur Beurre.",
            "{} - {}"
        )

        al_id = self._safety_answers(
            "Veuillez indiquer le numéro de l'aliment que vous souhaitez évaluer.\n",
            [prod.id for prod in products.array]
        )

        self._search_subst(al_id)


    def _search_subst(self, al_id):
        os.system('cls')
        data = self.db.load_data(al_id, product_view="Yes")

        substitutes = self.db.load_table(
            "aliments",
            f"WHERE id != {data.id} AND cat_id = {data.cat_id} AND nutriscore <= '{data.nutriscore}'",
            f"\nles produits suivants sont de bons substituts pour {data.name}:\n",
            "{} - {} (nutriscore: {})"
        )

        conclusion = self._safety_answers(
            "Quelle action souhaitez-vous entreprendre?\n"
            "Entrez le numéro d'un produit alternatif "
            "pour afficher le détail de sa composition.\n"
            "OU\n"
            "MP - Revenir au menu principal.\n"
            "00 - Quitter l'application.\n",
            [s.id for s in substitutes.array] + ["MP", "00"]
        )
        if conclusion == "MP":
            self.main()
            return
        elif conclusion == "00":
            self._quit()
            return
        else:
            subst = self.db.load_data(conclusion, product_view="Yes")

        conclusion = self._safety_answers(
            "\n\n"
            "Voulez-vous:\n"
            "1  - Choisir ce produit comme substitut.\n"
            "OU\n"
            "2  - Revenir au choix de substituts.\n"
            "MP - Revenir au menu principal.\n"
            "00 - Quitter l'application.\n",
            ["1", "2", "MP", "00"]
        )
        if conclusion == "1":
            self.db._save_subst(data, subst)
            self._search_subst(data.id)
        elif conclusion == "MP":
            self.main()
        elif conclusion == "00":
            self._quit()
        else:
            self._search_subst(data.id)


    def _quit(self):
        print(
            "Merci d'avoir choisi Pur Beurre"
            " dans votre lutte pour un alimentation plus saine!\n"
            "Nous espérons vous revoir bientôt."
        )
        self.db.close()
        return


    def _show_subst(self):
        substitutions = self.db.load_table(
            "substitutions",
            intro="Voici, pour chaque produit"
                  " le produits de substitution"
                  " que vous avez sauvegardés:"
        )
        for prod_id, subst_id in substitutions.array:
            print(f"{self.db.load_data(prod_id).name} - {self.db.load_data(subst_id).name}")
        
        ans = self._safety_answers(
            "Que souhaitez-vous faire?\n"
            "MP - Menu Principal\n"
            "00 - Quitter le programme.\n",
            ["MP", "00"]
        )
        if ans == "MP":
            self.main()
        elif ans == "00":
            self._quit()


    def _safety_answers(self, question, answers):
        """Ask a question and verify that it is rightly answered."""
        answers = [str(a) for a in answers]
        ans = input(question)
        while ans not in answers:
            print("Je suis désolé, je n'ai pas compris votre réponse.")
            ans = input(question)
        return ans


if __name__ == "__main__":
    main = Engine()
    main.main()