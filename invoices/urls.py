from django.urls import path
from .views import InvoiceView

urlpatterns = [
    path('invoices/', InvoiceView.as_view(), name='invoice-list-create'),
    path('invoices/<int:pk>/', InvoiceView.as_view(), name='invoice-update'),
]
