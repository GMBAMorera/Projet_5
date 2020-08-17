""" Array is a mysql table or subtable,
made for mass extraction of data.
"""


class Array:
    """All sorts of matrix, where each row is a set of data,
    from the given table and aranged like instructed.
    """

    def __init__(self, arr, instruction, table):
        """ array: table or subtable.
        instruction: instruction string for querying the connector.
        table: the table on wich is created the array.
        """
        self.array = arr
        self.instruction = instruction
        self.table = table