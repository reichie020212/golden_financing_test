import requests
from django.views.generic import UpdateView
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.parsers import MultiPartParser
from loan_calculator.forms import LoanInquiryForm
from loan_calculator.models import CustomerInfo
from loan_calculator.models import LoanInquiry
from loan_calculator import serializers
from loan_calculator.utils import calculate_monthly_amortization
from loan_calculator.utils import calculate_principal_amount
from loan_calculator.utils import calculate_rate_per_period
from loan_calculator.utils import calculate_total_interest
from loan_calculator.utils import calculate_total_payment
from loan_calculator.utils import get_first_loan_payment_date
from loan_calculator.utils import get_loan_maturity_date


class LoanCalculatorView(UpdateView):
    form_class = LoanInquiryForm
    template_name = 'loan_calculator.html'
    url_name = 'loan_calculator_url'
    model = LoanInquiry

    def get_object(self):
        pk = self.kwargs.get('pk') or None
        loan_inquiry = LoanInquiry.objects.filter(pk=pk).first()
        return loan_inquiry

    def form_valid(self, form):
        url = 'http://%s%s' % (self.request.META['HTTP_HOST'], reverse('loan_calculator_api'))
        form.cleaned_data['phone_number'] = str(form.cleaned_data['phone_number'])
        r = requests.post(url=url, json=form.cleaned_data)
        if r.status_code == 201:
            loan_request_id = r.json()[0].get('id')
            return redirect(reverse(self.url_name, kwargs={'pk': loan_request_id}))
        return redirect(reverse(self.url_name, kwargs=self.kwargs))


class LoanCalculatorAPIView(generics.CreateAPIView):
    parser_classes = [
        JSONParser
    ]
    parser_classes = [
        MultiPartParser,
        JSONParser
    ]
    serializer_class = serializers.LoanCalculatorSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            loan_inquiry = self.perform_create(serializer)
            return Response(
                LoanInquiry.objects.filter(pk=loan_inquiry.pk).values(
                    'id',
                    'customer_info__first_name',
                    'customer_info__middle_name',
                    'customer_info__last_name',
                    'customer_info__name_suffix',
                    'customer_info__email',
                    'customer_info__phone_number',
                    'customer_info__city',
                    'customer_info__province',
                    'customer_info',
                    'loan_type',
                    'principal_amount',
                    'monthly_amortization',
                    'total_interest',
                    'loan_term',
                    'total_sum_of_payments',
                    'first_loan_payment_date',
                    'loan_maturity_date',
                ),
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response({'error': 'Invalid Input.'}, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        first_name = serializer.validated_data.pop('first_name')
        last_name = serializer.validated_data.pop('last_name')
        if 'middle_name' in serializer.validated_data:
            middle_name = serializer.validated_data.pop('middle_name')
        else:
            middle_name = ''

        if 'name_suffix' in serializer.validated_data:
            name_suffix = serializer.validated_data.pop('name_suffix')
        else:
            name_suffix = ''
        email = serializer.validated_data.pop('email')
        phone_number = serializer.validated_data.pop('phone_number')
        city = serializer.validated_data.pop('city')
        province = serializer.validated_data.pop('province')
        loan_type = serializer.validated_data.get('loan_type')
        loan_term = serializer.validated_data.get('loan_term')
        rate_per_period = calculate_rate_per_period()

        if loan_type == 'type_a':
            principal_amount = serializer.validated_data.get('principal_amount')
            monthly_amortization = calculate_monthly_amortization(
                principal_amount=principal_amount,
                rate_per_period=rate_per_period,
                loan_term=loan_term,
            )
        else:
            monthly_amortization = serializer.validated_data.get('monthly_amortization')
            principal_amount = calculate_principal_amount(
                monthly_amortization=monthly_amortization,
                rate_per_period=rate_per_period,
                loan_term=loan_term,
            )

        total_interest = calculate_total_interest(
            principal_amount=principal_amount,
            monthly_amortization=monthly_amortization,
            loan_term=loan_term,
        )

        total_sum_of_payments = calculate_total_payment(
            principal_amount=principal_amount,
            total_interest=total_interest,
        )

        first_loan_payment_date = get_first_loan_payment_date()
        loan_maturity_date = get_loan_maturity_date(
            first_loan_payment_date,
            loan_term,
        )

        customer_info, created = CustomerInfo.objects.get_or_create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            city=city,
            province=province,
            defaults={
                'middle_name': middle_name,
                'name_suffix': name_suffix,
            }
        )

        loan_inquiry = serializer.save(
            customer_info=customer_info,
            principal_amount=principal_amount,
            monthly_amortization=monthly_amortization,
            total_interest=total_interest,
            total_sum_of_payments=total_sum_of_payments,
            first_loan_payment_date=first_loan_payment_date,
            loan_maturity_date=loan_maturity_date,
        )

        return loan_inquiry

    def get(self, request, *args, **kwargs):
        loan_type = self.request.GET.get('loan_type') or None
        qs = LoanInquiry.objects.all()

        if loan_type and loan_type not in ['type_a', 'type_b']:
            return Response(
                'loan type %s is invalid' % (loan_type),
                status=status.HTTP_400_BAD_REQUEST,
            )
        if loan_type:
            qs = qs.filter(loan_type=loan_type)
        return Response(qs.values(
            'customer_info__first_name',
            'customer_info__middle_name',
            'customer_info__last_name',
            'customer_info__name_suffix',
            'customer_info__email',
            'customer_info__phone_number',
            'customer_info__city',
            'customer_info__province',
            'customer_info',
            'loan_type',
            'principal_amount',
            'monthly_amortization',
            'total_interest',
            'loan_term',
            'total_sum_of_payments',
            'first_loan_payment_date',
            'loan_maturity_date',
        ))
