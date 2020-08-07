DB_NAME = "pur_beurre"
TABLES = dict()
TABLES['aliments'] = (
    "CREATE TABLE aliments ("
    "    id TINYINT NOT NULL AUTO_INCREMENT,"
    "    nom VARCHAR(100) NOT NULL,"
    "    cat_id TINYINT NOT NULL,"
    "    nutriscore CHAR(1) NOT NULL,"
    "    ingrédients TEXT,"
    "    saved TINYINT"
    "    PRIMARY KEY (id)"
    "    ) ENGINE = InnoDB"
)
TABLES['categories'] = (
    "CREATE TABLE categories ("
    "    cat_id TINYINT NOT NULL,"
    "    nom VARCHAR(50) NOT NULL,"
    "    PRIMARY KEY (cat_id)"
    "    ) ENGINE = InnoDB"
)


CATEGORIES = [
    'pizzas',
    'salades-composees',
    'fromages',
    'pates-à-tartiner-au-chocolat',
    'cereales-pour-petit-déjeuner'
]

MAX_PRODUITS = 20

URL = "https://fr.openfoodfacts.org"