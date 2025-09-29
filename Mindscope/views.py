from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
import logging

from .models import Screening, MoodEntry, ChatMessage, WellnessTip
from .utils.openai_client import generate_chat_response
from .utils.fallback_responses import get_fallback_response

logger = logging.getLogger(__name__)


def LandingPage(request):
    return render(request, "pages/LandingPage.html")


def home(request):
    return render(request, "pages/home.html")


def signup_view(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("signup")

        if User.objects.filter(username=full_name).exists():
            messages.error(request, "This name is already registered.")
            return redirect("signup")

        user = User.objects.create_user(username=full_name, password=password)
        login(request, user)
        messages.success(request, "Account created successfully!")
        return redirect("home")

    return render(request, "pages/signup.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        if not User.objects.filter(username=username).exists():
            messages.error(request, "No account found for this username.")
            return redirect("login")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Welcome back, {username}!")
            return redirect("home")
        else:
            messages.error(request, "Incorrect password.")
            return redirect("login")

    return render(request, "pages/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def dashboard(request):
    screenings = Screening.objects.filter(user=request.user).order_by("-date_taken")[:5]
    moods = MoodEntry.objects.filter(user=request.user).order_by("-date_logged")[:7]
    tips = WellnessTip.objects.all()[:3]
    
    return render(request, "pages/Dashboard.html", {
        "screenings": screenings,
        "moods": moods,
        "tips": tips,
    })


@login_required
def screening_tests(request):
    return render(request, "pages/ScreeningTests.html")


# ---------------- PHQ-9 ----------------
@login_required
def phq9_view(request):
    if request.method == "POST":
        score = sum(int(request.POST.get(f"q{i}", 0)) for i in range(1, 10))

        if score <= 4:
            severity = "Minimal"
            recommendations = [
                "Maintain your healthy lifestyle habits",
                "Stay socially connected",
                "Keep monitoring your mood",
            ]
        elif score <= 9:
            severity = "Mild"
            recommendations = [
                "Practice self-care and relaxation techniques",
                "Track your mood daily",
                "Seek support if symptoms persist",
            ]
        elif score <= 14:
            severity = "Moderate"
            recommendations = [
                "Consider speaking with a counselor",
                "Use our mood tracker regularly",
                "Explore mindfulness or breathing exercises",
            ]
        elif score <= 19:
            severity = "Moderately Severe"
            recommendations = [
                "Consider speaking with a mental health professional",
                "Track your mood daily using our mood tracker",
                "Explore our wellness resources for self-care tips",
            ]
        else:
            severity = "Severe"
            recommendations = [
                "Seek professional help as soon as possible",
                "Reach out to supportive friends/family",
                "Use wellness and crisis resources available",
            ]

        # Save to DB
        Screening.objects.create(
            user=request.user,
            screening_type="PHQ9",
            score=score,
            severity=severity,
        )

        return render(request, "pages/PHQ9_result.html", {
            "score": score,
            "severity": severity,
            "recommendations": recommendations,
        })

    return render(request, "pages/PHQ9.html")


# ---------------- GAD-7 ----------------
@login_required
def gad7_view(request):
    if request.method == "POST":
        score = sum(int(request.POST.get(f"q{i}", 0) or 0) for i in range(1, 8))

        if score <= 4:
            severity = "Minimal Anxiety"
            recommendations = [
                "Maintain healthy routines like sleep and exercise",
                "Practice daily relaxation techniques",
                "Stay socially engaged",
            ]
        elif score <= 9:
            severity = "Mild Anxiety"
            recommendations = [
                "Use mindfulness or breathing exercises",
                "Track triggers in a journal",
                "Talk with friends/family for support",
            ]
        elif score <= 14:
            severity = "Moderate Anxiety"
            recommendations = [
                "Consider seeking therapy or counseling",
                "Practice stress management strategies",
                "Incorporate regular physical activity",
            ]
        else:
            severity = "Severe Anxiety"
            recommendations = [
                "Reach out to a mental health professional promptly",
                "Use crisis hotlines if needed",
                "Build a strong support system with trusted people",
            ]

        # Save to DB
        Screening.objects.create(
            user=request.user,
            screening_type="GAD7",
            score=score,
            severity=severity,
        )

        return render(request, "pages/GAD7_result.html", {
            "score": score,
            "severity": severity,
            "recommendations": recommendations,
        })

    return render(request, "pages/GAD7.html")


# ---------------- PSS-10 ----------------
@login_required
def pss10_view(request):
    if request.method == "POST":
        answers = {}
        for i in range(1, 11):
            try:
                answers[i] = int(request.POST.get(f"q{i}", 0) or 0)
            except ValueError:
                answers[i] = 0

        reverse_items = {4, 5, 7, 8}
        total = 0
        for i in range(1, 11):
            v = answers[i]
            total += (4 - v) if i in reverse_items else v

        if total <= 13:
            severity = "Low"
            recommendations = [
                "Maintain healthy daily routines (sleep, diet, exercise).",
                "Practice brief daily relaxation (deep breathing, progressive muscle relaxation).",
                "Keep social connections and monitor stress regularly.",
            ]
        elif total <= 26:
            severity = "Moderate"
            recommendations = [
                "Use stress reduction practices (mindfulness, scheduled breaks).",
                "Establish a consistent sleep and exercise routine.",
                "Consider talking with a counselor or trusted person about stressors.",
            ]
        else:
            severity = "High"
            recommendations = [
                "Reach out to a mental health professional for assessment and support.",
                "Talk to supportive friends/family and reduce high-demand tasks if possible.",
                "If you feel overwhelmed or unsafe, contact local crisis services or emergency help immediately.",
            ]

        # Save to DB
        Screening.objects.create(
            user=request.user,
            screening_type="PSS10",
            score=total,
            severity=severity,
        )

        return render(request, "pages/PSS10_result.html", {
            "score": total,
            "severity": severity,
            "recommendations": recommendations,
        })

    return render(request, "pages/PSS10.html")


# ---------------- Mood Tracker ----------------
@login_required
def mood_tracker(request):
    if request.method == "POST":
        mood = request.POST["mood"]
        influencers = request.POST.get("influencers", "")
        notes = request.POST.get("notes", "")
        
        MoodEntry.objects.create(
            user=request.user,
            mood=mood,
            influencers=influencers,
            notes=notes,
        )
        messages.success(request, "Mood logged successfully!")
        return redirect("moodtracker")
    
    entries = MoodEntry.objects.filter(user=request.user).order_by("-date_logged")
    return render(request, "pages/moodtracker.html", {"entries": entries})


# ---------------- AI Chatbot ----------------
@login_required
def chat_view(request):
    if request.method == "POST":
        user_msg = request.POST.get("message", "").strip()
        if not user_msg:
            messages.error(request, "Please enter a message.")
            return redirect("chat")

        # Build conversation history
        recent_messages = ChatMessage.objects.filter(
            user=request.user
        ).order_by("-timestamp")[:6]
        
        history = []
        for msg in reversed(recent_messages):
            history.append({"role": "user", "content": msg.message})
            if msg.response:
                history.append({"role": "assistant", "content": msg.response})

        # Get AI response using the new hybrid approach
        try:
            from .utils.chat_engine import generate_intelligent_response
            ai_response = generate_intelligent_response(user_msg, history_messages=history)
        except Exception as e:
            logger.error(f"Error generating AI response: {e}")
            # Fallback to basic response if everything fails
            from .utils.fallback_responses import get_fallback_response
            ai_response = get_fallback_response(user_msg)
            messages.info(request, "Using fallback responses due to technical issues.")

        # Save to database
        ChatMessage.objects.create(
            user=request.user, 
            message=user_msg, 
            response=ai_response
        )
        
        return redirect("chat")

    # Get chat history for display
    chats = ChatMessage.objects.filter(user=request.user).order_by("timestamp")
    return render(request, "pages/AIChatbot.html", {"chats": chats})

def learn_more(request):
    return render(request, "pages/learn_more.html")