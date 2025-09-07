from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from app_account.forms import CustomUserCreationForm, CustomUserLoginForm
from app_account.models import CustomUser



from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from app_account.forms import CustomUserCreationForm
from app_account.models import CustomUser

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
            user.save()

            # Verified check
            if not user.is_verified:
                messages.success(request, "Your account created successfully. Please verify your email before logging in.")
                return redirect('login')
            else:
                login(request, user)
                messages.success(request, f"Registration successful! Welcome, {user.email}!")
                return redirect('home')
        else:
            # Show all form errors as messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')  # username = email
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)

            if user:
                if not user.is_verified:
                    messages.warning(request, "⚠️ Your account is not verified. Please check your email.")
                    return redirect('login')

                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name or user.email}!")
                return redirect('home')
            else:
                messages.error(request, "❌ User Not Found!.")
        else:
            messages.error(request, "Invalid email or password.")
    else:
        form = CustomUserLoginForm()

    return render(request, 'registration/login.html', {'form': form})



def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('login')
