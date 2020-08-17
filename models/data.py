"""Data class is the archetype of a row inside the aliment table.
Can also, sometimes, be used for categorie table, by analogy.
"""

class Data:
    """ Class of data, as seen in Pur Beurre database."""

    def __init__(self, identity, name,
                 nutriscore=None, ingredients=None, cat_id=None):
        """ As per the columns of aliment's table."""
        self.id = identity
        self.name = name
        self.nutriscore = nutriscore
        self.ingredients = ingredients
        self.cat_id = cat_id
        self.iterate = (self.id, self.name,
                        self.nutriscore, self.ingredients, self.cat_id)

    def __iter__(self):
        self.i = -1
        return self

    def __next__(self):
        self.i += 1
        if self.i == len(self.iterate):
            raise StopIteration
        return self.iterate[self.i]
