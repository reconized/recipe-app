from django.core.exceptions import ValidationError
from decouple import config, Csv
import re

def validate_no_profanity(value):
    profanity_list = config('BAD_WORDS', cast=Csv())
    pattern = re.compile(r'\b(' + '|'.join(profanity_list) + r')\b', re.IGNORECASE)

    if pattern.search(value):
        raise ValidationError("This content contains inappropriate language and is not allowed.")