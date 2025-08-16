from django.core.exceptions import ValidationError
from decouple import config, Csv
from apps.recipes.constants import FRACTION_PATTERN
import re

def validate_no_profanity(value):
    profanity_list = config('BAD_WORDS', cast=Csv())
    pattern = re.compile(r'\b(' + '|'.join(profanity_list) + r')\b', re.IGNORECASE)

    if pattern.search(value):
        raise ValidationError("This content contains inappropriate language and is not allowed.")
    
def validate_quantity_format(value):
    """
    Validate quantity string only contains numbers, whitespace and forward slashes.
    """
    if re.search(r'[^\d\s/]', value):
        raise ValidationError(
            'Quantity must contain only numbers, spaces, and a slash for fractions.'
        )
    
def validate_quantity(value):
    if not FRACTION_PATTERN.match(value):
        raise ValidationError(
            "Quantity must be a number or fraction (e.g., '1', '1/2', '2 1/2')."
        )