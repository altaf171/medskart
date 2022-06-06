import re
from rest_framework import serializers
def password_complex_validator(password):
    regex_pattern = "^(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[^\w\d\s:])([^\s]){8,16}$"
    if not re.search(regex_pattern, password):
        raise serializers.ValidationError("Enter 8 or longer digit complex password.")
