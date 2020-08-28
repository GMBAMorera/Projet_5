"""Contains all basic operation on the database:
read, insert and update on it.
All higher level operation (create, fill and erase)
are on initdatabase.py.
"""

from models.array import Array
from models.data import Data
from database.initdatabase.initdatabase import InitDataBase

from database.instructions import (
    SELECT_DATA, SELECT_TABLE, SELECT_SUBST,
    UPDATE_SUBST, INSERT_SUBST
)
from discussions import (
    PRODUCT_VIEW, VALID_SUBST, SEPARATOR,
    SUBST_FORMAT, SUBST_PRESENTATION
)


class DataBase(InitDataBase):

    def __init__(self):
        """ Go fetch the connector for querying mysql table."""
        super().__init__()

    def load_data(self, identity, product_view=None):
        """Select a data inside the aliments table,
        searching with its id.
        """
        self.cursor.execute(SELECT_DATA.format(identity))
        for c in self.cursor:
            data =  Data(*c)

        if product_view is not None:
            print(
                PRODUCT_VIEW.format(data.name, data.nutriscore,
                                    data.ingredients)
            )
        return data

    def load_table(self, table, instruction="", intro=None, line=None):
        """ Select data into DB following the given instruction,
        print them and finally ask for the use of it if necessary.
        WARNING: the column order of the query must match exactly
        the order of printing.
        """
        self.cursor.execute(
            " ".join((SELECT_TABLE.format(table), instruction))
        )

        if intro is not None:
            print(intro)

        arr = [Data(*c) for c in self.cursor]

        if line is not None:
            for a in arr:
                print(line.format(*a))

        return Array(arr, instruction, table)

    def save_subst(self, prod, subst):
        """Update substitution table with new subst data."""
        try:
            self.cursor.execute(INSERT_SUBST.format(prod.id, subst.id))
            self.cnx.commit()
        except Exception:
            self.cursor.execute(UPDATE_SUBST.format(subst.id, prod.id))
            self.cnx.commit()
        print(VALID_SUBST.format(subst.name, prod.name))

    def print_subst(self):
        """Show the substitution table."""
        self.cursor.execute(SELECT_SUBST)

        print(SEPARATOR)
        print(SUBST_PRESENTATION)
        for c in self.cursor:
            print(SUBST_FORMAT.format(*c))