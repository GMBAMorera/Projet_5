import os
import time

from database.database import DataBase
from discussions import (
    WELCOME, GOODBYE, CATEGORIES_PRESENTATION,
    SELECT_CAT, AL_PRESENTATION, SELECT_AL,
    PRESENT_SUBST, SUBST_PRESENTATION, M_1, M_2, MP, Q, I,
    MAIN_MENU, SUBST_MENU, SAVE_MENU, MAIN_OR_QUIT,
    SAVE_ANSWERS, MAIN_ANSWERS, BACK_ANSWERS,
    ID_NAME_FORMAT, ID_NAME_NUTR_FORMAT, NOT_AN_ANSWER
)
from database.instructions import (
    TABLE_CAT, TABLE_AL, TABLE_SUBST, ALL_CAT_AL, ALL_SUBST_AL, VOID
)

class Engine(DataBase):
    """ Main class, running the Pur Beurre application."""
    
    def __init__(self):
        super().__init__()

    def main(self):
        os.system("cls")

        print(WELCOME)
        a = self._safety_answers(MAIN_MENU, MAIN_ANSWERS)

        if a == M_1:
            self._search_subst()
        elif a == M_2:
            self._show_subst()
        elif a == Q:
            self._quit()
        elif a == I:
            self.initialize()
            self.main()

    def _search_subst(self, al_id=None):
        if al_id is None:
            cat_id = self._search_cat()
            al_id = self._search_prod(cat_id)

        os.system("cls")
        data = self.load_data(al_id, product_view="Yes")

        substitutes = self.load_table(
            TABLE_AL,
            ALL_SUBST_AL.format(data.id, data.cat_id, data.nutriscore),
            PRESENT_SUBST.format(data.name),
            ID_NAME_NUTR_FORMAT
        )
        subst = self._select_subst(substitutes)
        if subst is not None:
            self._join_save(data, subst)

    def _search_cat(self):
        # Choose between categories
        categories = self.load_table(
            TABLE_CAT,
            VOID,
            CATEGORIES_PRESENTATION,
            ID_NAME_FORMAT
        )

        cat_id = self._safety_answers(
            SELECT_CAT,
            [cat.id for cat in categories.array]
        )
        return cat_id

    def _search_prod(self, cat_id):
        os.system("cls")

        # Choose between products
        products = self.load_table(
            TABLE_AL,
            ALL_CAT_AL.format(cat_id),
            AL_PRESENTATION,
            ID_NAME_FORMAT
        )

        al_id = self._safety_answers(
            SELECT_AL,
            [prod.id for prod in products.array]
        )
        return al_id

    def _select_subst(self, substitutes):
        conclusion = self._safety_answers(
            SUBST_MENU,
            [s.id for s in substitutes.array] + BACK_ANSWERS
        )
        if conclusion == MP:
            self.main()
            return None
        elif conclusion == Q:
            self._quit()
            return None
        else:
            subst = self.load_data(conclusion, product_view="Yes")
            return subst

    def _join_save(self, data, subst):
        conclusion = self._safety_answers(SAVE_MENU, SAVE_ANSWERS)
        if conclusion == M_1:
            self.save_subst(data, subst)
            time.sleep(3)
            self._search_subst(data.id)
        elif conclusion == MP:
            self.main()
        elif conclusion == Q:
            self._quit()
        else:
            self._search_subst(data.id)

    def _quit(self):
        print(GOODBYE)
        self.close()
        return

    def _show_subst(self):
        self.print_subst()

        ans = self._safety_answers(MAIN_OR_QUIT, BACK_ANSWERS)
        if ans == MP:
            self.main()
        elif ans == Q:
            self._quit()

    def _safety_answers(self, question, answers):
        """Ask a question and verify that it is rightly answered."""
        answers = [str(a) for a in answers]
        ans = input(question)
        while ans not in answers:
            print(NOT_AN_ANSWER)
            ans = input(question)
        return ans


if __name__ == "__main__":
    main = Engine()
    try:
        main.main()
    except:
        main.erase()