from requests import get
import mysql
from mysql.connector import errorcode

from constants import DB_NAME, TABLES, CATEGORIES, MAX_PRODUITS, URL

def create_database():
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

    try:
        cursor.execute("USE {}".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Database {} does not exists.".format(DB_NAME))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database()
            print("Database {} created successfully.".format(DB_NAME))
            cnx.database = DB_NAME
        else:
            print(err)
            exit(1)

def create_tables():
    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")


def get_data():
    aliments = []
    for cat_id, cat in enumerate(CATEGORIES):
        n_al = 0
        n_page = 1
        while n_al != MAX_PRODUITS:
            al_list = get(URL + f'category/{cat}/{n_page}.json')
            al_list = al_list.json()
            al_list = al_list['products']
            if len(al_list) == 0:
                break

            n_try = 0
            while n_al != 20 or n_try !=len(al_list):
                next_try = al_list[n_try]
                try:
                    name = next_try['product_name']
                    nutriscore = next_try['nutrition_grade_fr']
                    ingredients = next_try['ingredients_text_fr']
                except KeyError:
                    n_try += 1
                    continue

                if name == cat or name in [n for (n,_,_,_) in aliments]:
                    n_try += 1
                    continue

                aliments.append((name, cat_id, nutriscore, ingredients))
                n_try += 1
                n_al += 1

            n_page += 1
    return aliments


def feed_tables(aliments):
    instructions = (
            "INSERT INTO categories "
            "(nom)"
            "VALUES "
    )
    for cat in CATEGORIES:
        instructions + "({}),".format(cat)

    cursor.execute(instructions)

    instructions = (
            "INSERT INTO aliments "
            "(nom, cat_id, nutriscore, ingredients)"
            "VALUES "
    )
    for al in aliments:
        instructions + "({}, {}, {}, {}),".format(*al)

    cursor.execute(instructions)


def set_database():

    # Creating database
    create_database()

    # Creating tables
    create_tables()

    # Get data from Open Food Facts and insert them into tables
    aliments = get_data()
    feed_tables(aliments)



if __name__ == "__main__":
    global cnx, cursor
    cnx = mysql.connector.connect(user='root', password="8&4Douze!")
    cursor = cnx.cursor()

    set_database()

    cnx.close()
    cursor.close()