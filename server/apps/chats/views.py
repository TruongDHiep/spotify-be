# chats/views.py
import os
import json
import requests
from dotenv import load_dotenv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

load_dotenv()

class ChatWithDeepSeekView(APIView):
    def post(self, request):
        try:
            # Handle either a single message or a conversation history
            messages = request.data.get("messages", [])

            # If no messages provided or empty messages array
            if not messages:
                return Response({"error": "Missing messages"}, status=status.HTTP_400_BAD_REQUEST)

            openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
            if not openrouter_api_key:
                return Response({"error": "Missing API key"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {openrouter_api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "http://localhost:3000",
                    "X-Title": "MyChatApp",
                },
                data=json.dumps({
                    "model": "meta-llama/llama-4-scout:free",
                    "messages": messages,
                    "max_tokens": 1000,  # Giới hạn độ dài response
                    "temperature": 0.7,  # Điều chỉnh độ sáng tạo của response
                })
            )

            # Check if the request was successful
            if response.status_code != 200:
                return Response({
                    "error": f"API request failed with status code {response.status_code}",
                    "details": response.text
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            result = response.json()
            print("API Response:", json.dumps(result, indent=2))  # Log detailed response
            
            # Extract reply with better error handling
            if "choices" not in result or not result["choices"]:
                return Response({
                    "error": "Invalid response format from API",
                    "details": result
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
            reply = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            if not reply:
                return Response({
                    "error": "Empty reply from API",
                    "details": result
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({"reply": reply})

        except Exception as e:
            import traceback
            print("Exception:", str(e))
            print(traceback.format_exc())
            return Response({
                "error": str(e),
                "traceback": traceback.format_exc()
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)