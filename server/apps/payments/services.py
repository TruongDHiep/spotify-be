from django.shortcuts import get_object_or_404
from .models import Payment
from apps.users.models import User
class PaymentService:

    @staticmethod
    def get_payment_by_id(payment_id):
        """Get a specific payment by ID"""
        return get_object_or_404(Payment, id=payment_id)
    
    @staticmethod
    def create_payment(data):
        user = get_object_or_404(User, id=data["user_id"])
        Payment.objects.create(
            user=user,
            amount=data["amount"],
            pay_date=data["pay_date"],
            expr_date=data["expr_date"],
            status=data["status"],
        )
    
    @staticmethod
    def delete_payment(payment_id):
        """Delete a payment"""
        payment = get_object_or_404(Payment, id=payment_id)
        payment.delete()