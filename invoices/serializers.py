from rest_framework import serializers
from .models import Invoice, InvoiceDetail

class InvoiceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceDetail
        fields = ['id', 'description', 'quantity', 'price', 'line_total']

    def validate(self, data):
        # Ensure line_total is correct
        if data['line_total'] != data['quantity'] * data['price']:
            raise serializers.ValidationError("Line total must be equal to quantity multiplied by price.")
        return data

class InvoiceSerializer(serializers.ModelSerializer):
    details = InvoiceDetailSerializer(many=True)

    class Meta:
        model = Invoice
        fields = ['id', 'invoice_number', 'customer_name', 'date', 'details']

    def create(self, validated_data):
        print("Creating a new invoice with details:", validated_data)
        details_data = validated_data.pop('details')
        invoice = self._create_invoice(validated_data)
        self._create_invoice_details(invoice, details_data)
        return invoice

    def update(self, instance, validated_data):
        print(f"Updating invoice {instance.id} with data:", validated_data)
        details_data = validated_data.pop('details')
        self._update_invoice(instance, validated_data)
        self._replace_invoice_details(instance, details_data)
        return instance

    def _create_invoice(self, validated_data):
        # Create an Invoice instance
        return Invoice.objects.create(**validated_data)

    def _create_invoice_details(self, invoice, details_data):
        # Create InvoiceDetail instances linked to the invoice
        for detail_data in details_data:
            InvoiceDetail.objects.create(invoice=invoice, **detail_data)

    def _update_invoice(self, instance, validated_data):
        # Update the Invoice instance
        instance.invoice_number = validated_data.get('invoice_number', instance.invoice_number)
        instance.customer_name = validated_data.get('customer_name', instance.customer_name)
        instance.date = validated_data.get('date', instance.date)
        instance.save()

    def _replace_invoice_details(self, instance, details_data):
        # Replace existing InvoiceDetail instances with new data
        instance.details.all().delete()
        self._create_invoice_details(instance, details_data)
