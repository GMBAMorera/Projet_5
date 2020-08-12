DB_NAME = "pur_beurre"

PRODUCTS_FIELDS = {
    'product_name_fr': "name",
    'nutrition_grade_fr': "nutriscore",
    'ingredients_text_fr': "ingredients"
}


TABLES = dict()
TABLES['aliments'] = (
    "CREATE TABLE aliments ("
    "    id TINYINT NOT NULL AUTO_INCREMENT,"
    "    name VARCHAR(100) NOT NULL,"
    "    nutriscore CHAR(1) NOT NULL,"
    "    ingredients LONGTEXT NOT NULL,"
    "    cat_id TINYINT NOT NULL,"
    "    PRIMARY KEY (id)"
    "    ) ENGINE = InnoDB "
    "    DEFAULT CHARACTER SET = utf8"
)
TABLES['categories'] = (
    "CREATE TABLE categories ("
    "    cat_id TINYINT NOT NULL AUTO_INCREMENT,"
    "    nom VARCHAR(50) NOT NULL,"
    "    PRIMARY KEY (cat_id)"
    "    ) ENGINE = InnoDB "
    "    DEFAULT CHARACTER SET = utf8"
)
TABLES['substitutions'] = (
    "CREATE TABLE substitutions("
    "    prod_id TINYINT NOT NULL,"
    "    subst_id TINYINT NOT NULL,"
    "    PRIMARY KEY (prod_id)"
    "    ) ENGINE = InnoDB "
    "    DEFAULT CHARACTER SET = utf8"
)

CATEGORIES = [
    'pizzas',
    'salades-composees',
    'fromages',
    'pates-a-tartiner',
    'cereales-pour-petit-déjeuner'
]

URL = "https://fr.openfoodfacts.org/cgi/search.pl"
MAX_PRODUCTS_IMPORT = 50
MAX_PRODUCTS_KEEPED = 20