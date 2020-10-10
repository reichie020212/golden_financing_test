from django.db import models
from model_utils import Choices
from phonenumber_field.modelfields import PhoneNumberField
from model_utils.models import TimeStampedModel


class CustomerInfo(TimeStampedModel):
    first_name = models.CharField(
        max_length=100,
    )
    middle_name = models.CharField(
        max_length=100,
        blank=True,
    )
    last_name = models.CharField(
        max_length=100,
    )
    name_suffix = models.CharField(
        max_length=50,
        blank=True,
    )
    email = models.EmailField(
        max_length=254,
    )
    phone_number = PhoneNumberField(
        max_length=50,
    )
    city = models.CharField(
        max_length=100,
    )
    province = models.CharField(
        max_length=100,
    )

    class Meta:
        unique_together = [(
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'city',
            'province',
        )]


class LoanInquiry(TimeStampedModel):
    LOAN_TYPE_CHOICES = Choices(
        ('type_a', 'Type A'),
        ('type_b', 'Type B'),
    )
    customer_info = models.ForeignKey(
        'CustomerInfo',
        on_delete=models.CASCADE,
    )
    loan_type = models.CharField(
        max_length=254,
        choices=LOAN_TYPE_CHOICES,
    )
    principal_amount = models.DecimalField(
        decimal_places=2,
        max_digits=18,
    )
    monthly_amortization = models.DecimalField(
        decimal_places=2,
        max_digits=18,
    )
    total_interest = models.DecimalField(
        decimal_places=2,
        max_digits=18,
    )
    loan_term = models.PositiveIntegerField()
    total_sum_of_payments = models.DecimalField(
        decimal_places=2,
        max_digits=18,
    )
    first_loan_payment_date = models.DateField()
    loan_maturity_date = models.DateField()
