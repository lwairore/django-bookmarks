from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from . import forms

# Create your views here.
def user_login(request):
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=['password']) # hecks user credentials and returns a User object if they are right
            if user is not None:
                if user.is_active:
                    login(request, user) # sets the user in the current session.
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = forms.LoginForm()
    return render(request, 'account/login.html', {'form': form})