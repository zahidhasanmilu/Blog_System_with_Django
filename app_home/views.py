from django.shortcuts import render

# Login MIXIN
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def home_view(request):
    return render(request, 'home.html')