from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Invoice
from .serializers import InvoiceSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.

class InvoiceView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'invoice_number': openapi.Schema(type=openapi.TYPE_STRING, example="INV001"),
                'customer_name': openapi.Schema(type=openapi.TYPE_STRING, example="John Doe"),
                'date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, example="2024-11-12"),
                'details': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'description': openapi.Schema(type=openapi.TYPE_STRING, example="Product A"),
                            'quantity': openapi.Schema(type=openapi.TYPE_INTEGER, example=2),
                            'price': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, example=50.00),
                            'line_total': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, example=100.00),
                        }
                    )
                ),
            }
        ),
        responses={status.HTTP_201_CREATED: InvoiceSerializer}
    )
    def post(self, request):
        serializer = InvoiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        print(f"Received PUT request for invoice {pk} with data:", request.data)
        try:
            invoice = Invoice.objects.get(pk=pk)
        except Invoice.DoesNotExist:
            print(f"Invoice {pk} not found.")
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = InvoiceSerializer(invoice, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        print("Validation errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
