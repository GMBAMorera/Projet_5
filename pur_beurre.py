import mysql
from Database import Database

from constants import DB_NAME

class Engine:
    """ Main class, running the Pur Beurre application."""


    def __init__(self):
        self.db = Database()


    def main(self):
        print(
            "\n\n"
            "Bienvenue dans l'application Pur Beurre!\n"
            "\n"
        )
        try:
            a = self._safety_answers(
                "Que souhaitez-vous faire?\n"
                "1    - Rechercher un substitut à un produit.\n"
                "2    - lire la liste des substituts.\n"
                "00   - Quitter le programme.\n"
                "Init - Initialiser ou Réinitialiser la base de donnée.\n",
                ["1", "2", "00", "Init"]
            )

            if a == "1":
                self._search_subst()
            elif a == "2":
                self._show_subst()
            elif a == "00":
                self._quit()
            elif a == "Init":
                self.db.initialize()
        except:
            self.db.cursor.execute(f"DROP DATABASE {DB_NAME}")
            raise


    def _search_subst(self):
        # Choose between categories
        categories = self.db.load_table(
            "categories",
            "",
            "Voici la liste des catégories suivis par notre plateforme:",
            "{} - {}"
        )

        cat_id = self._safety_answers(
            "Veuillez indiquer le numéro de la catégorie que vous souhaitez évaluer.\n",
            [str(cat[0]) for cat in categories.array]
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
            [str(prod.id) for prod in products.array]
        )
        data = self.db.load_data(al_id)
        self._product_view(data)
        substitutes = self.db.load_table(
            "aliments",
            f"WHERE id != {data.id} AND cat_id = {data.cat_id} AND nutriscore <= {data.nutriscore}",
            f"\nles produits suivants sont de bons remplaçants pour {data.name}:\n",
            "{} - {} (nutriscore: {})"
        )

        subst = None
        while True:
            if subst == None:
                conclusion = self._safety_answers(
                    "Quelle action souhaitez-vous entreprendre?\n"
                    "Entrez le numéro d'un produit de substitution"
                    "pour afficher le détail de sa composition.\n\n"
                    "OU\n\n"
                    "MP - Revenir au menu principal\n"
                    "00 - Quitter l'application",
                    [s.id for s in substitutes.array] + ["MP", "00"]
                )
                if conclusion == "MP":
                    self.main()
                elif conclusion == "00":
                    self._quit()
                else:
                    subst = self.db.load_data(conclusion)
                    self._product_view(subst)
            else:
                conclusion = self._safety_answers(
                    "Quelle action souhaitez-vous entreprendre?\n"
                    "Entrez le numéro d'un produit de substitution"
                    "pour afficher le détail de sa composition.\n\n"
                    "OU\n\n"
                    " S - Sauvegarder le substitut choisi\n"
                    "MP - Revenir au menu principal\n"
                    "00 - Quitter l'application",
                    [s.id for s in substitutes.array] + ["S", "MP", "00"]
                )
                if conclusion == "S":
                    self._save_subst(data, subst)
                elif conclusion == "MP":
                    self.main()
                elif conclusion == "00":
                    self._quit()
                else:
                    subst = self.db.load_data(conclusion)
                    self._product_view(subst)


    def _quit(self):
        self.db.close()
        exit(1)


    def _show_subst(self):
        pass


    def _save_subst(self, prod, subst):
        try:
            self.db.cursor.execute(
                "UPDATE substitions"
                f" SET subst_id={subst.id}"
                f" WHERE prod_id={prod.id}"
            )
        except:
            self.db.cursor.execute(
                "INSERT INTO substitutions"
                f"VALUES ({subst.id}, {prod.id})"
            )
        print(f"{subst.name} a bien été enregistré comme le produit de susbtition de {prod.name}")


    def _product_view(self, data):
        print(
            f"{data.name} a le nutriscore suivant: {data.nutriscore}\n"
            "Il est composé de:\n"
            f"{data.ingredients}\n"
        )


    def _safety_answers(self, question, answers):
        """Ask a question and verify that it is rightly answered."""
        ans = input(question)
        while ans not in answers:
            print("Je suis désolé, je n'ai pas compris votre réponse.")
            ans = input(question)
        return ans


if __name__ == "__main__":
    main = Engine()
    main.main()