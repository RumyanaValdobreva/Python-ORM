from django.core.exceptions import ValidationError


def validate_customer_name(value):
    for letter in value:
        if not (letter.isalpha() or letter.isspace()):
            raise ValidationError("Name can only contain letters and spaces")


def validate_customer_phone_number(value):
    if not value.startswith('+359') or len(value) != 13:
        raise ValidationError("Phone number must start with '+359' followed by 9 digits")
