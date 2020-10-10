from django import forms
from decimal import Decimal
from loan_calculator.models import LoanInquiry
from phonenumber_field.formfields import PhoneNumberField


class LoanInquiryForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100)
    middle_name = forms.CharField(max_length=100, required=False)
    last_name = forms.CharField(max_length=100)
    name_suffix = forms.CharField(max_length=50, required=False)
    email = forms.EmailField(max_length=100)
    phone_number = PhoneNumberField(
        error_messages = {'invalid': 'Enter a valid phone number (e.g. +639xxxxxxxxx)'},
    )
    city = forms.CharField(max_length=100)
    province = forms.CharField(max_length=100)

    LOAN_TERM_CHOICES = [(x, x) for x in range(3, 19)]
    loan_term = forms.ChoiceField(
        required=True,
        choices=LOAN_TERM_CHOICES,
    )

    class Meta:
        model = LoanInquiry
        fields = [
            'loan_type',
            'principal_amount',
            'monthly_amortization',
            'loan_term',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

        self.fields['loan_type'].label = 'Select your desired Loan Type'
        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name (required)'
        self.fields['middle_name'].widget.attrs['placeholder'] = 'Middle Name (optional)'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name (required)'
        self.fields['name_suffix'].widget.attrs['placeholder'] = 'Suffix (optional)'
        self.fields['email'].widget.attrs['placeholder'] = 'e.g. sample@yopmail.com'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'format: +639xxxxxxxxx'
        self.fields['principal_amount'].required = False
        self.fields['principal_amount'].widget.attrs['placeholder'] = "Minimum of Php 10,000.00"
        self.fields['monthly_amortization'].required = False
        self.fields['monthly_amortization'].widget.attrs['placeholder'] = "Minimum of Php 1,000.00"

        if self.instance and self.instance.pk:
            self.fields['first_name'].initial = self.instance.customer_info.first_name
            self.fields['middle_name'].initial = self.instance.customer_info.middle_name
            self.fields['last_name'].initial = self.instance.customer_info.last_name
            self.fields['name_suffix'].initial = self.instance.customer_info.name_suffix
            self.fields['email'].initial = self.instance.customer_info.email
            self.fields['phone_number'].initial = self.instance.customer_info.phone_number
            self.fields['city'].initial = self.instance.customer_info.city
            self.fields['province'].initial = self.instance.customer_info.province

    def clean(self):
        cleaned_data = super().clean()
        loan_type = cleaned_data.get('loan_type')
        principal_amount = cleaned_data.get('principal_amount')
        monthly_amortization = cleaned_data.get('monthly_amortization')
        loan_term = int(cleaned_data.get('loan_term'))

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
            raise forms.ValidationError(errors)

        if not principal_amount:
            cleaned_data['principal_amount'] = 0
        if not monthly_amortization:
            cleaned_data['monthly_amortization'] = 0

        return cleaned_data
