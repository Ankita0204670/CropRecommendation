from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import pickle
import numpy as np
import csv
from .models import CropRecord , UserProfile, Feedback
from django.contrib.auth.models import User
from .forms import FeedbackForm
from django.http import HttpResponse
from django.urls import reverse
from urllib.parse import urlencode
from django.db import transaction
from django.db.models import Avg
import re

# Load your ML model
model = pickle.load(open('model.pkl', 'rb'))

num_to_label = {}
try:
    with open('label_name_number.csv', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            num_to_label[int(row['number'])] = row['label']
except Exception:
    num_to_label = {}

# Home page
def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

# Predict Crop Page
@login_required
def predict(request):
    prediction = None

    if request.method == "POST":
        nitrogen = float(request.POST['nitrogen'])
        phosphorus = float(request.POST['phosphorus'])
        potassium = float(request.POST['potassium'])
        temperature = float(request.POST['temperature'])
        humidity = float(request.POST['humidity'])
        ph = float(request.POST['ph'])
        rainfall = float(request.POST['rainfall'])

        data = np.array([[nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]])
        prediction = model.predict(data)[0]
        label = num_to_label.get(int(prediction), str(prediction))

        with transaction.atomic():
            CropRecord.objects.create(
                farmer=request.user,
                N=nitrogen,
                P=phosphorus,
                K=potassium,
                temperature=temperature,
                humidity=humidity,
                ph=ph,
                rainfall=rainfall,
                predicted_crop=label,
            )

        messages.success(request, f"Prediction saved: {label}")
        request.session['prediction'] = label
        request.session['last_values'] = {
            'N': nitrogen,
            'P': phosphorus,
            'K': potassium,
            'temperature': temperature,
            'humidity': humidity,
            'ph': ph,
            'rainfall': rainfall,
        }
        url = reverse('result')
        return redirect(f"{url}?" + urlencode({'p': label}))

    return render(request, "predict.html")

# Result Page
@login_required
def result(request):
    predicted_crop = request.GET.get('p') or request.session.get('prediction')
    if not predicted_crop:
        latest = CropRecord.objects.filter(farmer=request.user).order_by('-recommended_on').first()
        if latest:
            predicted_crop = latest.predicted_crop
        else:
            messages.error(request, "No prediction found. Please predict first.")
            return redirect('predict')
    values = request.session.get('last_values')
    if not values:
        latest = CropRecord.objects.filter(farmer=request.user).order_by('-recommended_on').first()
        if latest:
            values = {
                'N': latest.N,
                'P': latest.P,
                'K': latest.K,
                'temperature': latest.temperature,
                'humidity': latest.humidity,
                'ph': latest.ph,
                'rainfall': latest.rainfall,
            }
    warnings = []
    if values:
        N = float(values.get('N', 0))
        P = float(values.get('P', 0))
        K = float(values.get('K', 0))
        TEMP = float(values.get('temperature', 0))
        HUM = float(values.get('humidity', 0))
        PH = float(values.get('ph', 0))
        RAIN = float(values.get('rainfall', 0))
        if N < 50: warnings.append("Nitrogen level is low")
        if P < 30: warnings.append("Phosphorus level is low")
        if K < 30: warnings.append("Potassium level is low")
        if N > 120: warnings.append("Nitrogen level is high")
        if P > 80: warnings.append("Phosphorus level is high")
        if K > 80: warnings.append("Potassium level is high")
        if TEMP < 15 or TEMP > 40: warnings.append("Temperature out of ideal range")
        if HUM < 30 or HUM > 90: warnings.append("Humidity out of ideal range")
        if PH < 5.5 or PH > 8.0: warnings.append("Soil pH may be unsuitable")
        if RAIN < 50 or RAIN > 350: warnings.append("Rainfall out of ideal range")
    return render(request, 'result.html', {'prediction': predicted_crop, 'warnings': warnings})


# Researcher dashboard
@login_required
def researcher(request):
    profile = UserProfile.objects.filter(user=request.user).first()
    if not request.user.is_superuser and (not profile or profile.role != 'Researcher'):
        return HttpResponse("Unauthorized")

    crop_filter = request.GET.get('crop', '').strip()
    records = CropRecord.objects.all().order_by('-recommended_on')
    if crop_filter:
        records = records.filter(predicted_crop__iexact=crop_filter)

    agg = records.aggregate(avg_N=Avg('N'), avg_P=Avg('P'), avg_K=Avg('K'))

    return render(request, 'researcher.html', {
        'records': records,
        'avg_N': agg.get('avg_N'),
        'avg_P': agg.get('avg_P'),
        'avg_K': agg.get('avg_K'),
    })

# User Registration
def register(request):
    if request.method == "POST":
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        full_name = request.POST.get('fullName', '').strip()
        mobile = request.POST.get('mobile', '').strip()
        if (not first_name or not last_name) and full_name:
            parts = full_name.split()
            if parts:
                first_name = parts[0]
                last_name = " ".join(parts[1:]) if len(parts) > 1 else ""
        role = request.POST.get('usertype', '').strip()
        if not email or not password or not role or not (first_name and last_name) or not mobile:
            messages.error(request, "All fields are required.")
            return render(request, 'register.html')
        if not re.fullmatch(r'\d{10}', mobile):
            messages.error(request, "Mobile number must be exactly 10 digits.")
            return render(request, 'register.html')
        try:
            if User.objects.filter(username=email).exists():
                messages.error(request, "Account already exists. Please log in.")
                return redirect('login')
            user = User.objects.create_user(username=email, email=email, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            if role:
                try:
                    UserProfile.objects.create(user=user, role=role)
                except Exception:
                    pass
            messages.success(request, "Registration successful! Please log in.")
            return redirect('login')
        except Exception as e:
            messages.error(request, f"Could not register: {e}")
            return render(request, 'register.html')
    return render(request, 'register.html')


# User Login
def custom_login(request):
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        role_hint = request.POST.get('usertype', '').strip()
        if not username or not password or not role_hint:
            messages.error(request, "All fields are required.")
            return render(request, 'login.html')
        user = authenticate(username=username, password=password)
        if user is not None:
            try:
                profile = UserProfile.objects.filter(user=user).first()
            except Exception:
                profile = None
            actual_role = 'Admin' if user.is_superuser else (profile.role if profile else None)
            if not user.is_superuser and actual_role and actual_role != role_hint:
                messages.error(request, "Incorrect user role")
                return render(request, 'login.html')
            login(request, user)
            messages.info(request, f"You are now logged in as {username}.")
            request.session['username'] = user.username
            request.session['usertype'] = actual_role or role_hint
            if (actual_role or role_hint) == 'Farmer':
                return redirect('predict')
            if (actual_role or role_hint) == 'Researcher':
                return redirect('researcher')
            return redirect('home')
        messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')

# User Logout
@login_required
def user_logout(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('home')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        new_password = request.POST.get('new_password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()
        if not email or not new_password or not confirm_password:
            messages.error(request, "All fields are required.")
            return render(request, 'forgot.html')
        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'forgot.html')
        try:
            user = User.objects.get(username=email)
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password reset successful. Please log in.")
        except User.DoesNotExist:
            messages.error(request, "No account found for that email.")
        return redirect('login')
    return render(request, 'forgot.html')

def feedback(request):
    form = FeedbackForm(request.POST or None)

    if request.method == "POST":
        subject = request.POST.get('subject')
        message_text = request.POST.get('message')
        rating = request.POST.get('rating')

        if not subject or not message_text or not rating:
            messages.error(request, "Fill all fields")
            return render(request, 'feedback.html', {'form': form})

        if form.is_valid():
            feedback_instance = form.save(commit=False)
            if request.user.is_authenticated:
                feedback_instance.user = request.user
            feedback_instance.save()
            messages.success(request, "Thank you for your feedback!")
            return redirect('feedback')

    return render(request, 'feedback.html', {'form': form})

@login_required
def feedback_list(request):
    if not request.user.is_superuser:
        return HttpResponse("Unauthorized")
    feedbacks = Feedback.objects.all().order_by('-created_at')
    return render(request, 'feedback_list.html', {'feedbacks': feedbacks})

