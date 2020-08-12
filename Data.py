import mysql


class Data:
    """ Class of data, as seen in Pur Beurre database."""


    def __init__(self, identity, name, nutriscore, ingredients, cat_id):
        self.id = identity
        self.name = name
        self.nutriscore = nutriscore
        self.ingredients = ingredients
        self.cat_id = cat_id
        self.print = f"({identity}, '{name}', '{nutriscore}', '{ingredients}', {cat_id})"
        self.iterate = (self.id, self.name, self.nutriscore, self.ingredients, self.cat_id)