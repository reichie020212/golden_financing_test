from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^loan_calculator/$', views.LoanCalculatorAPIView.as_view(), name='loan_calculator_api'),
    url(r'^(?P<pk>\d+)/$', views.LoanCalculatorView.as_view(), name='loan_calculator_url'),
    url(r'^', views.LoanCalculatorView.as_view(), name='loan_calculator_url'),
]
