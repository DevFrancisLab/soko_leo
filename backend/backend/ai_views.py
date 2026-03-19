import sys
from pathlib import Path

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

# Add parent directory to path so we can import ai module
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from ai.markets_agent import get_ai_response


class AIChatView(APIView):
    """Simple AI chat endpoint for frontend integration."""

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        question = request.data.get("question") or request.data.get("message")
        if not question:
            return Response({"detail": "question is required."}, status=status.HTTP_400_BAD_REQUEST)

        location = request.data.get("location", "Kenya")
        season = request.data.get("season", "current")

        answer = get_ai_response(question, location=location, season=season)
        return Response({"answer": answer})
