import phonenumbers
from phonenumber_field import phonenumber
from rest_framework import serializers


class PhoneNumberField(serializers.CharField):
    def to_internal_value(self, value):
        if value:
            try:
                phone = phonenumber.PhoneNumber.from_string(value)
                if phonenumbers.is_valid_number(phone):
                    return phone
            except phonenumbers.NumberParseException:
                pass
            raise serializers.ValidationError('Not a valid phone number.')
