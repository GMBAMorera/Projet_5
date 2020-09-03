
CREATE DATABASE pur_beurre DEFAULT CHARACTER SET 'utf8';
CREATE TABLE categories (
    cat_id TINYINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL
    ) ENGINE = InnoDB 
    DEFAULT CHARACTER SET = utf8
);
CREATE TABLE aliments (
    id TINYINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    nutriscore CHAR(1) NOT NULL,
    ingredients LONGTEXT NOT NULL,
    cat_id TINYINT NOT NULL,
    CONSTRAINT fk_cat
        FOREIGN KEY (cat_id)
        REFERENCES categories(cat_id)
    ) ENGINE = InnoDB 
    DEFAULT CHARACTER SET = utf8
);
CREATE TABLE substitutions(
    prod_id TINYINT NOT NULL PRIMARY KEY,
    subst_id TINYINT NOT NULL,
    CONSTRAINT fk_prod
        FOREIGN KEY (prod_id)
        REFERENCES aliments(id),
    CONSTRAINT fk_subst
        FOREIGN KEY (subst_id)
        REFERENCES aliments(id)
    ) ENGINE = InnoDB 
    DEFAULT CHARACTER SET = utf8
);
