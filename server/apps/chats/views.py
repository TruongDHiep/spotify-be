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
            user_message = request.data.get("message")

            if not user_message:
                return Response({"error": "Missing message"}, status=status.HTTP_400_BAD_REQUEST)

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
                    "model": "deepseek/deepseek-chat-v3-0324:free",
                    "messages": [
                        {
                            "role": "user",
                            "content": user_message
                        }
                    ],
                })
            )

            result = response.json()
            # print(result)
            reply = result.get("choices", [{}])[0].get("message", {}).get("content", "")

            return Response({"reply": reply})

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
