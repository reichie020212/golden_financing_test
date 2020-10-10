import datetime
from dateutil import relativedelta
from decimal import Decimal


def calculate_rate_per_period(annual_rate=Decimal('0.24')):
    return annual_rate / 12


def calculate_monthly_amortization(
    principal_amount,
    rate_per_period,
    loan_term,
):
    a = ((1 + rate_per_period) ** loan_term) - 1
    b = rate_per_period * ((1 + rate_per_period) ** loan_term)
    return round(principal_amount / (a / b), 1)


def calculate_principal_amount(
    monthly_amortization,
    rate_per_period,
    loan_term,
):
    a = (((1 + rate_per_period) ** loan_term) - 1)
    b = rate_per_period * ((1 + rate_per_period) ** loan_term)
    return round(monthly_amortization * (a / b), 1)


def calculate_total_interest(
    principal_amount,
    monthly_amortization,
    loan_term,
):
    return (monthly_amortization * loan_term) - principal_amount


def calculate_total_payment(
    principal_amount,
    total_interest,
):
    return principal_amount + total_interest


def get_first_loan_payment_date():
    current_date = datetime.datetime.now().date()
    if 1 <= current_date.day <= 15:
        return datetime.datetime(current_date.year, current_date.month, 7).date() + relativedelta.relativedelta(months=1)
    return datetime.datetime(current_date.year, current_date.month, 22).date() + relativedelta.relativedelta(months=1)


def get_loan_maturity_date(first_payment_date, loan_term):
    return first_payment_date + relativedelta.relativedelta(months=loan_term)
