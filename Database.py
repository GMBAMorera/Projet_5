import sys
from requests import get
import mysql
from mysql.connector import errorcode

from constants import TABLES, CATEGORIES, URL, MAX_PRODUCTS_IMPORT, MAX_PRODUCTS_KEEPED, PRODUCTS_FIELDS, DB_NAME
from Array import Array
from Data import Data

class Database:
    def __init__(self):
        self.max_produits = MAX_PRODUCTS_KEEPED

        self.cnx = mysql.connector.connect(user='root', password="8&4Douze!")
        self.cursor = self.cnx.cursor()

        try:
            self.cursor.execute(f"USE {DB_NAME}")
        except:
            print("loading database...")
            try:
                self.initialize()
                print("loading done\n\n\n\n")
            except:
                print("failed to load database, erasing...")
                self.cursor.execute(f"DROP DATABASE {DB_NAME}")
                print("database erased")
                raise


    def initialize(self):
        # Creating database
        self._create()

        # Creating tables
        self._formate()

        # Get data from Open Food Facts and insert them into tables
        aliments = self._find()
        self._fill(aliments)


    def load_data(self, identity):
        self.cursor.execute(
            "SELECT id, name, nutriscore, ingredients, cat_id FROM aliments "
            f"WHERE id = {identity}"
        )
        for c in self.cursor:
            return Data(*c)


    def load_table(self, table, instruction, intro, line):
        """ Select data into DB following the given instruction,
        print them and finally ask for the use of it if necessary.
        WARNING: the column order of the query must match exactly
        the order of printing."""
        self.cursor.execute(
            f"SELECT * FROM {table} "
            + instruction
        )

        print(intro)
        if table == 'aliments':
            arr = [Data(*c) for c in self.cursor]
            for a in arr:
                print(line.format(*a.iterate))
        else:
            arr = [c for c in self.cursor]
            for a in arr:
                print(line.format(*a))
        return Array(arr, instruction, table)


    def close(self):
        self.cursor.close()
        self.cnx.close()


    def _create(self):
        try:
            self.cursor.execute(f"DROP DATABASE {DB_NAME}")
        except:
            pass

        self.cursor.execute(
            f"CREATE DATABASE {DB_NAME} DEFAULT CHARACTER SET 'utf8'")

        self.cursor.execute(f"USE {DB_NAME}")


    def _formate(self):
        for table_name, table_instruction in TABLES.items():
            print(f"Creating table {table_name}")
            self.cursor.execute(table_instruction)


    def _find(self):
        aliments = []

        for cat_id, cat in enumerate(CATEGORIES):
            print(f'Beginning to find products for category {cat}')
            n_page = 0
            cat_al = []
            while len(cat_al) < MAX_PRODUCTS_KEEPED:
                import_al = self._scratch_category(cat, n_page)
                cat_al = self._try_aliment_list(cat, cat_id, cat_al, import_al, len(aliments))
                n_page += 1

            aliments += cat_al
            print(f"after seeing {n_page} page of products,"
                  f" the category {cat} is filled")
        return aliments


    def _fill(self, aliments):
        # Fill category table
        instructions = ", ".join([f"('{cat}')" for cat in CATEGORIES])
        instructions = (f"INSERT INTO categories (nom) VALUES {instructions}")
        self.cursor.execute(instructions)
        print("categories' table augmented")

        # Fill aliments table
        instructions = [al.print for al in aliments]
        print(instructions)
        instructions = ", ".join(instructions)
        instructions = (
            "INSERT INTO aliments"
            + " (id, name, nutriscore, ingredients, cat_id) VALUES"
            + instructions
        )
        self.cursor.execute(instructions)
        print("aliments' table augmented")


    def _scratch_category(self, cat, n_page):
        payload = {
            'action': 'process',
            'tagtype_0': 'categories',
            'tag_contains_0': 'contains',
            'tag_0': cat,
            'tagtype_1': 'nutrition_grade',
            'tag_contains_1': 'contains',
            'fields': ','.join(PRODUCTS_FIELDS.keys()),
            'page_size': n_page,
            'json': 'true',
        }

        al_list = get(URL, params=payload).json()
        return al_list['products']


    def _try_aliment_list(self, cat, cat_id, cat_al, long_aliments, n_al):
        aliments = []
        for al in long_aliments:
            try:
                if al['ingredients_text_fr'] == '':
                    continue
                prod = Data(
                    identity='NULL', #Will be automatically filled later
                    name=al['product_name_fr'].replace("'", " "),
                    nutriscore=al['nutrition_grade_fr'],
                    ingredients=al['ingredients_text_fr'].replace("'", " "),
                    cat_id=cat_id
                )
            except KeyError:
                continue

            if prod.name == cat or prod.name in [al.name for al in aliments]:
                continue

            aliments.append(prod)
            if len(cat_al) + len(aliments) == MAX_PRODUCTS_KEEPED:
                break
        return cat_al + aliments


if __name__ == "__main__":
    db = Database()
    db.close()