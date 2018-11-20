from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import SignUpForm, ProfileForm

def signup(request):
    if request.method == 'POST':
        userForm = SignUpForm(request.POST)
        profileForm = ProfileForm(request.POST, request.FILES)
        if userForm.is_valid() and profileForm.is_valid():
            user = userForm.save()
            profile = profileForm.save(commit=False)
            profile.user = user
            profile.save()
            username = userForm.cleaned_data.get('username')
            raw_password = userForm.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        userForm = SignUpForm()
        profileForm = ProfileForm()
    return render(request, 'registration/signup.html', {'signupForm': userForm, 'profileForm' : profileForm})