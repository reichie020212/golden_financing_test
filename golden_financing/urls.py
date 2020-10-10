from django.contrib import admin
from django.conf.urls import include
from django.conf.urls import url

urlpatterns = [
    url(r'admin/', admin.site.urls),
    url('', include('loan_calculator.urls')),
]
