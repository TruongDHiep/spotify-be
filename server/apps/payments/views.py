import uuid
import hmac
import hashlib
import requests
import json
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils.decorators import method_decorator
from .services import PaymentService  # Import service
from .models import Payment  # Nếu cần dùng model
from datetime import datetime
from .models import User

class PaymentView(APIView):
    permission_classes = [AllowAny]  # Cho phép test từ frontend

    def post(self, request):
        data = request.data
        amount = data.get("amount")
        order_info = data.get("orderInfo")
        user_id = data.get("userId")  # Lấy từ frontend
        pay_date_str = data.get("payDate")

        # Parse pay_date từ chuỗi "YYYY-MM-DD"
        pay_date = datetime.strptime(pay_date_str, "%Y-%m-%d").date()

        # Tính exprDate: cộng 30 ngày
        expr_date = pay_date + timedelta(days=30)

        # Lấy user từ DB
        user = get_object_or_404(User, id=user_id)
        endpoint = "https://test-payment.momo.vn/v2/gateway/api/create"
        partnerCode = "MOMO"
        accessKey = "F8BBA842ECF85"
        secretKey = "K951B6PE1waDMi640xX08PD3vg6EkVlz"
        redirectUrl = f"http://localhost:3000/user/payment/success?userId={user_id}&amount={amount}&payDate={pay_date}"
        ipnUrl = redirectUrl
        requestType = "payWithATM"
        orderId = str(uuid.uuid4())
        requestId = str(uuid.uuid4())
        extraData = ""

        raw_signature = (
            f"accessKey={accessKey}&amount={amount}&extraData={extraData}"
            f"&ipnUrl={ipnUrl}&orderId={orderId}&orderInfo={order_info}"
            f"&partnerCode={partnerCode}&redirectUrl={redirectUrl}"
            f"&requestId={requestId}&requestType={requestType}"
        )

        signature = hmac.new(
            bytes(secretKey, 'utf-8'),
            bytes(raw_signature, 'utf-8'),
            hashlib.sha256
        ).hexdigest()

        payload = {
            "partnerCode": partnerCode,
            "partnerName": "Test",
            "storeId": "MomoTestStore",
            "requestId": requestId,
            "amount": amount,
            "orderId": orderId,
            "orderInfo": order_info,
            "redirectUrl": redirectUrl,
            "ipnUrl": ipnUrl,
            "lang": "vi",
            "extraData": extraData,
            "requestType": requestType,
            "signature": signature
        }

        momo_response = requests.post(endpoint, json=payload, headers={'Content-Type': 'application/json'})
        result = momo_response.json()
        pay_url = result.get("payUrl")

        if pay_url:
            return Response({"payUrl": pay_url})
        return Response({"error": "Không thể tạo liên kết thanh toán."}, status=400)


@method_decorator(ensure_csrf_cookie, name='dispatch')
class CSRFTokenView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return JsonResponse({"message": "CSRF cookie set."})
    
class SavePaymentView(APIView):
    permission_classes = [AllowAny]  # Cho phép không đăng nhập

    def post(self, request):
        data = request.data
        user_id = data.get("userId")
        amount = data.get("amount")
        pay_date = data.get("payDate")
        expr_date = data.get("exprDate")
        status = data.get("status", "pending")

        if not user_id:
            return Response({"error": "Thiếu userId"}, status=400)

        # Lưu payment
        try:
            PaymentService.create_payment({
                "user_id": user_id,
                "amount": amount,
                "pay_date": pay_date,
                "expr_date": expr_date,
                "status": status
            })
            return Response({"success": 1})
        except Exception as e:
            return Response({"success": 0, "errormsg": str(e)}, status=500)

