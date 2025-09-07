from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from app_account.forms import CustomUserCreationForm, CustomUserLoginForm
from app_account.models import CustomUser

from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings

from django.shortcuts import get_object_or_404

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')

            # Check if email already exists
            if CustomUser.objects.filter(email=email).exists():
                messages.warning(request, 'Email already exists. Please use a different email.')
                return render(request, 'registration/register.html', {'form': form})

            user = form.save(commit=False)
            user.is_active = True
            user.is_verified = False
            user.save()

            # Verified check
            # Generate verification link
            verification_link = request.build_absolute_uri(
                reverse('verify_email', args=[user.id])  # we’ll create this view
            )

            # Send verification email
            send_mail(
                "Verify your account",
                f"Hi {user.email},\n\nClick the link to verify your account:\n{verification_link}",
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            messages.success(request, "✅ Account created! Check your email to verify before login.")
            return redirect('login')
        else:
            # Show all form errors as messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


def verify_email(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if not user.is_verified:
        user.is_verified = True
        user.save()
        messages.success(request, "🎉 Your email has been verified. You can now log in!")
    else:
        messages.info(request, "Your email is already verified.")
    return redirect('login')

def login_view(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')  # এটি form এ name="username" থাকার কারণে
            password = form.cleaned_data.get('password')
            
            # CustomUser এর জন্য
            user = authenticate(request, email=email, password=password)

            if user:
                if not user.is_verified:
                    messages.warning(request, "⚠️ Your account is not verified. Please check your email.")
                    return redirect('login')

                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name or user.email}!")
                return redirect('home')
            else:
                messages.error(request, "❌ User Not Found!")
        else:
            messages.error(request, "Invalid email or password.")
    else:
        form = CustomUserLoginForm()

    return render(request, 'registration/login.html', {'form': form})



def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('login')
