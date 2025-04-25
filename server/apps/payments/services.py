from django.shortcuts import get_object_or_404
from .models import Payment

class PaymentService:

    @staticmethod
    def get_payment_by_id(payment_id):
        """Get a specific payment by ID"""
        return get_object_or_404(Payment, id=payment_id)
    
    @staticmethod
    def create_payment(data):
        """Create a new payment"""
        payment = Payment.objects.create(**data)
        return payment
    
    @staticmethod
    def delete_payment(payment_id):
        """Delete a payment"""
        payment = get_object_or_404(Payment, id=payment_id)
        payment.delete()