"""All info needed for OpenFoodFact API searchs."""


PRODUCTS_FIELDS = {
    "product_name_fr": "name",
    "nutrition_grade_fr": "nutriscore",
    "ingredients_text_fr": "ingredients"
}

CATEGORIES = [
    "pizzas",
    "salades-composees",
    "fromages",
    "pates-a-tartiner",
    "cereales-pour-petit-déjeuner"
]

URL = "https://fr.openfoodfacts.org/cgi/search.pl"
MAX_PRODUCTS_KEEPED = 20