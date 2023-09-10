from django.core.exceptions import ValidationError
import re


class CustomPasswordValidator:
    def __init__(self, min_length=8, special_chars='!@#$%^&*()_+.'):
        self.min_length = min_length
        self.special_chars = special_chars

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError("Your password must contain at least 8 characters.")

        if password.isdigit():
            raise ValidationError("Your password can't be entirely numeric.")

        if not any(char in self.special_chars for char in password):
            raise ValidationError("Your password must contain at least onr special character: !@#$%^&*()_+.")

        #  More checks can be added

    def get_help_text(self):
        return (
            "Your password must contain at least 8 characters, "
            "not be entirely numeric, and include at least one special character: !@#$%^&*()_+."
        )

# Add this to settings.py in  AUTH_PASSWORD_VALIDATORS

# AUTH_PASSWORD_VALIDATORS = [
#     # ... (existing validators)
#     {
#         'NAME': 'your_app_name.validators.CustomPasswordValidator',
#         'OPTIONS': {
#             'min_length': 8,
#             'special_chars': '!@#$%^&*()_+',  # You can customize the special characters here
#         },
#     },
# ]
