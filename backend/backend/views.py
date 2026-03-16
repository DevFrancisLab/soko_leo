from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
import os
import requests

from ai_workflow import run_main_workflow


class MarketInsightView(APIView):
    """API endpoint that runs the LangGraph workflow for market insights."""

    # permission_classes = [IsAuthenticated]  # Temporarily disabled for testing

    def post(self, request, *args, **kwargs):
        market_data = request.data.get("market_data")
        weather_data = request.data.get("weather_data")
        crop_data = request.data.get("crop_data")

        if market_data is None or weather_data is None or crop_data is None:
            return Response(
                {"detail": "market_data, weather_data, and crop_data are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        result = run_main_workflow(market_data, weather_data, crop_data)
        return Response(result, status=status.HTTP_200_OK)


class AIChatView(APIView):
    """API endpoint for AI chat using Groq LLM."""

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_message = request.data.get("message")
        if not user_message:
            return Response(
                {"detail": "message is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Use Groq API for AI response
            groq_api_key = os.getenv('GROQ_API_KEY')
            if not groq_api_key:
                return Response({"response": "AI service temporarily unavailable."}, status=status.HTTP_200_OK)

            headers = {
                'Authorization': f'Bearer {groq_api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': 'llama3-8b-8192',
                'messages': [
                    {
                        'role': 'system',
                        'content': 'You are SokoLeo AI, a helpful farming assistant in Kenya. Provide advice on agriculture, markets, weather, and farming practices. Be friendly and practical.'
                    },
                    {
                        'role': 'user',
                        'content': user_message
                    }
                ],
                'max_tokens': 500,
                'temperature': 0.7
            }

            response = requests.post('https://api.groq.com/openai/v1/chat/completions', headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            ai_response = response.json()['choices'][0]['message']['content']
            
            return Response({"response": ai_response}, status=status.HTTP_200_OK)
            
        except requests.RequestException as e:
            return Response({"response": "Sorry, I'm having trouble connecting to the AI service. Please try again later."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"response": "An error occurred. Please try again."}, status=status.HTTP_200_OK)
