import re

UNIT_CHOICES = [
    ('tsp', 'Teaspoon'),
    ('tbsp', 'Tablespoon'),
    ('c', 'Cup'),
    ('pt', 'Pint'),
    ('qt', 'Quart'),
    ('gal', 'Gallon'),
    ('fl', 'Fluid ounce'),
    ('oz', 'Ounce'),
    ('lb', 'Pound'),
    ('dash', '1/8 teaspoon'),
    ('pinch', 'Pinch'),
    ('stick', 'Stick'),
    ('mL', 'Milliliter'),
    ('L', 'Liter'),
    ('kg', 'Kilogram'),
    ('g', 'Gram'),
]

FRACTION_PATTERN = re.compile(r'^\s*\d+(\s+\d+/\d+|\s*/\d+|/\d+)?\s*$')