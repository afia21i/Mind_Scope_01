"""
URL configuration for SWE project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from Mindscope import views   # import views directly from your app

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.LandingPage, name="landingpage"),
    path("home/", views.home, name="home"),
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("screening-tests/", views.screening_tests, name="screening_tests"),
    path("screening/phq9/", views.phq9_view, name="phq9"),
    path("screening/gad7/", views.gad7_view, name="gad7"),
    path("screening/pss10/", views.pss10_view, name="pss10"),
    path("mood-tracker/", views.mood_tracker, name="mood_tracker"),
    path("chat/", views.chat_view, name="chat"),
    path("learn-more/", views.learn_more, name="learn_more"),
]

