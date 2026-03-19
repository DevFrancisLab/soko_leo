"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home'
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import sys
from pathlib import Path

from django.contrib import admin
from django.urls import include, path

# Add parent directory to path for ai module imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from .ai_views import AIChatView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/ai/chat/', AIChatView.as_view(), name='ai_chat'),
    path('api/accounts/', include('accounts.urls')),
]
