""" All mysql instruction that the cursor will execute
during initialisation and work upon Pur Beurre.
"""


### DATABASE.PY ###
SELECT_DATA = (
    "SELECT id, name, nutriscore, ingredients, cat_id FROM aliments"
    " WHERE id = {}"
)
SELECT_TABLE = "SELECT * FROM {}"

UPDATE_SUBST = (
    "UPDATE substitions"
    " SET subst_id={} WHERE prod_id={}"
)
INSERT_SUBST = (
    "INSERT INTO substitutions"
    " VALUES ({}, {})"
)
SELECT_SUBST = (
    "SELECT prod.name, subst.name"
    " FROM substitutions"
    " INNER JOIN aliments as prod"
    " ON substitutions.prod_id = prod.id"
    " INNER JOIN aliments as subst"
    " ON substitutions. subst_id = subst.id"
)


### INITDATABASE.PY ###
USER = "root"
PASSWORD = "8&4Douze!"
DB_NAME = "pur_beurre"

USE = "USE {}"
DROP = "DROP DATABASE {}"
CREATE = "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'"

CAT_ROW = "(NULL, '{}')"
FILL_CAT = "INSERT INTO categories (cat_id, name) VALUES {}"

AL_ROW = "({}, '{}', '{}', '{}', {})"
INSERT_AL = (
    "INSERT INTO aliments"
    " (id, name, nutriscore, ingredients, cat_id) VALUES"
)

TABLES = dict()
TABLES['categories'] = (
    "CREATE TABLE categories ("
    "    cat_id TINYINT AUTO_INCREMENT PRIMARY KEY,"
    "    name VARCHAR(50) NOT NULL"
    "    ) ENGINE = InnoDB "
    "    DEFAULT CHARACTER SET = utf8"
)
TABLES['aliments'] = (
    "CREATE TABLE aliments ("
    "    id TINYINT AUTO_INCREMENT PRIMARY KEY,"
    "    name VARCHAR(100) NOT NULL,"
    "    nutriscore CHAR(1) NOT NULL,"
    "    ingredients LONGTEXT NOT NULL,"
    "    cat_id TINYINT NOT NULL,"
    "    CONSTRAINT fk_cat"
    "        FOREIGN KEY (cat_id)"
    "        REFERENCES categories(cat_id)"
    "    ) ENGINE = InnoDB "
    "    DEFAULT CHARACTER SET = utf8"
)
TABLES['substitutions'] = (
    "CREATE TABLE substitutions("
    "    prod_id TINYINT NOT NULL,"
    "    subst_id TINYINT NOT NULL,"
    "    CONSTRAINT fk_prod"
    "        FOREIGN KEY (prod_id)"
    "        REFERENCES aliments(id),"
    "    CONSTRAINT fk_subst"
    "        FOREIGN KEY (subst_id)"
    "        REFERENCES aliments(id)"
    "    ) ENGINE = InnoDB "
    "    DEFAULT CHARACTER SET = utf8"
)


### MAIN.PY ###
TABLE_CAT = "categories"
TABLE_AL = "aliments"
TABLE_SUBST = "substitutions"

ALL_CAT_AL = "WHERE cat_id={}"
ALL_SUBST_AL = "WHERE id != {} AND cat_id = {} AND nutriscore <= '{}'"
VOID = ""
SPACE = " "