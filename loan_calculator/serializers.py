from decimal import Decimal
from rest_framework import serializers
from loan_calculator.models import LoanInquiry
from loan_calculator.fields import PhoneNumberField


class LoanCalculatorSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        required=True,
    )
    middle_name = serializers.CharField(
        required=False,
        allow_blank=True,
    )
    last_name = serializers.CharField(
        required=True,
    )
    name_suffix = serializers.CharField(
        required=False,
        allow_blank=True,
    )
    email = serializers.EmailField(
        required=True,
    )
    phone_number = PhoneNumberField(
        required=True,
    )
    city = serializers.CharField(
        required=True,
    )
    province = serializers.CharField(
        required=True,
    )
    principal_amount = serializers.DecimalField(
        max_digits=18,
        decimal_places=2,
        required=False,
        default=0,
    )
    monthly_amortization = serializers.DecimalField(
        max_digits=18,
        decimal_places=2,
        required=False,
        default=0,
    )

    class Meta:
        model = LoanInquiry
        fields = [
            'loan_type',
            'principal_amount',
            'monthly_amortization',
            'loan_term',
            'first_name',
            'middle_name',
            'last_name',
            'name_suffix',
            'email',
            'phone_number',
            'city',
            'province',
        ]

    def validate(self, data):
        loan_type = data.get('loan_type')
        principal_amount = data.get('principal_amount')
        monthly_amortization = data.get('monthly_amortization')
        loan_term = data.get('loan_term')

        errors = {}
        if loan_type == 'type_a':
            if not principal_amount:
                errors.update({
                    'principal_amount': 'Principal Amount is required if loan type is Type A.'
                })
            elif principal_amount < Decimal('10000'):
                errors.update({
                    'principal_amount': 'Minimum of PHP 10,000.00'
                })
            if not (3 <= loan_term <= 18):
                errors.update({
                    'loan_term': 'Loan term for Type A should be from 3 months to 18 months with 3 months interval.'
                })
            elif loan_term % 3 != 0:
                errors.update({
                    'loan_term': 'Loan term for Type A should be 3, 6, 9, 12, 15, or 18.'
                })

        if loan_type == 'type_b':
            if not monthly_amortization:
                errors.update({
                    'monthly_amortization': 'monthly_amortization is required if loan_type is Type B.'
                })
            elif monthly_amortization < Decimal('1000'):
                errors.update({
                    'monthly_amortization': 'Minimum of PHP 1,000.00'
                })
            if not (6 <= loan_term <= 18):
                errors.update({
                    'loan_term': 'Loan term for Type A should be from 6 months to 18 months.'
                })

        if errors:
            raise serializers.ValidationError(errors)
        return data
