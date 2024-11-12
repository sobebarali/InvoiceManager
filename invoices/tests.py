from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Invoice, InvoiceDetail

class InvoiceAPITestCase(APITestCase):
    def setUp(self):
        self.invoice_data = {
            "invoice_number": "INV001",
            "customer_name": "John Doe",
            "date": "2024-11-12",
            "details": [
                {
                    "description": "Product A",
                    "quantity": 2,
                    "price": 50.00,
                    "line_total": 100.00
                },
                {
                    "description": "Product B",
                    "quantity": 1,
                    "price": 75.00,
                    "line_total": 75.00
                }
            ]
        }
        self.invoice = Invoice.objects.create(
            invoice_number="INV002",
            customer_name="Jane Doe",
            date="2024-11-13"
        )
        InvoiceDetail.objects.create(
            invoice=self.invoice,
            description="Product C",
            quantity=3,
            price=30.00,
            line_total=90.00
        )

    def test_create_invoice(self):
        url = reverse('invoice-list-create')
        response = self.client.post(url, self.invoice_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Invoice.objects.count(), 2)
        self.assertEqual(InvoiceDetail.objects.count(), 3)

    def test_update_invoice(self):
        url = reverse('invoice-update', args=[self.invoice.id])
        response = self.client.put(url, self.invoice_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Invoice.objects.get(id=self.invoice.id).customer_name, "John Doe")
        self.assertEqual(InvoiceDetail.objects.filter(invoice=self.invoice).count(), 2)
