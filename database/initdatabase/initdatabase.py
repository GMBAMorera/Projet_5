from requests import get
from mysql.connector import connect
import time

from database.initdatabase.config import (
    USER, PASSWORD, CATEGORIES, URL,
    MAX_PRODUCTS_IMPORT, MAX_PRODUCTS_KEEPED,
    PRODUCTS_FIELDS, DB_NAME
)
from database.instructions import (
    TABLES, DROP, USE, CREATE, CAT_ROW, TABLE_AL,
    FILL_CAT, SELECT_TABLE, TABLE_CAT, AL_ROW, INSERT_AL
)
from discussions import (
    INIT_DB, FAIL_INIT_DB, ERASE_DB, SUCCESS_INIT_DB,
    CREATE_TB, CREATE_TB_SUCCESS,
    CAT_FINDING, CAT_FINDING_FAIL, CAT_FINDING_SUCCESS, 
)


class InitDataBase:
    def __init__(self):

        self.cnx = connect(user=USER, password=PASSWORD)
        self.cursor = self.cnx.cursor()

        try:
            self.cursor.execute(USE.format(DB_NAME))
        except:
            print(INIT_DB)
            try:
                self.initialize()
            except:
                print(FAIL_INIT_DB)
                self.erase()
                raise

    def close(self):
        self.cursor.close()
        self.cnx.close()

    def erase(self):
        self.cursor.execute(DROP.format(DB_NAME))
        print(ERASE_DB)


    def initialize(self):
        # Creating database
        self._create()

        # Creating tables
        self._formate()
        self._fill_categories()

        # Get data from Open Food Facts
        # and insert them into the table aliments
        aliments = self._find()
        self._fill(aliments)

        print(SUCCESS_INIT_DB)
        time.sleep(3)

    def _create(self):
        try:
            self.cursor.execute(DROP.format(DB_NAME))
        except:
            pass

        self.cursor.execute(CREATE.format(DB_NAME))

        self.cursor.execute(USE.format(DB_NAME))

    def _formate(self):
        for table_name, table_instruction in TABLES.items():
            print(CREATE_TB.format(table_name))
            self.cursor.execute(table_instruction)

    def _fill_categories(self):
        # Fill category table
        instructions = ", ".join([CAT_ROW.format(cat) for cat in CATEGORIES])
        instructions = (FILL_CAT.format(instructions))
        self.cursor.execute(instructions)
        print(CREATE_TB_SUCCESS.format(TABLE_CAT))

    def _find(self):
        self.cursor.execute(SELECT_TABLE.format(TABLE_CAT))

        aliments = []
        for cat_id, cat in self.cursor:
            print(CAT_FINDING.format(cat))
            n_page = 0
            cat_al = []
            al_name = []
            while len(cat_al) < MAX_PRODUCTS_KEEPED:
                import_al = self._scratch_category(cat, n_page)
                if len(import_al) == 0:
                    raise CAT_FINDING_FAIL.format(cat)

                cat_al = self._try_aliment_list(cat, cat_id, cat_al,
                                                import_al, al_name)
                n_page += 1

            aliments += cat_al
            print(CAT_FINDING_SUCCESS.format(n_page, cat))
        return aliments

    def _try_aliment_list(self, cat, cat_id, cat_al, long_aliments, al_name):
        for al in long_aliments:
            try:
                product, name, ing = self.create_row(al, cat_id)
            except KeyError:
                continue

            if name == cat or name in [a for a in al_name] or ing == '':
                continue

            cat_al.append(product)
            if len(cat_al) == MAX_PRODUCTS_KEEPED:
                break

            al_name.append(name)
        return cat_al

    def create_row(self, al, cat_id):
        row = (
            "NULL",
            al['product_name_fr'].replace("'", " "),
            al['nutrition_grade_fr'].upper(),
            al['ingredients_text_fr'].replace("'", " "),
            cat_id
        )
        name = row[1]
        ing = row[3]
        return AL_ROW.format(*row), name, ing

    def _scratch_category(self, cat, n_page):
        payload = {
            "action": "process",
            "tagtype_0": "categories",
            "tag_contains_0": "contains",
            "tag_0": cat,
            "tagtype_1": "nutrition_grade",
            "tag_contains_1": "contains",
            "fields": ",".join(PRODUCTS_FIELDS.keys()),
            "page_size": n_page,
            "json": "true",
        }

        al_list = get(URL, params=payload).json()
        return al_list["products"]

    def _fill(self, aliments):
        # Fill aliments table
        aliments = ", ".join(aliments)
        instructions = " ".join((INSERT_AL, aliments)) 
        self.cursor.execute(instructions)
        print(CREATE_TB_SUCCESS.format(TABLE_AL))
