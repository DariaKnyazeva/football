from django.contrib.auth import login, authenticate

from django.shortcuts import render, redirect

from .forms import UserCreationForm

from django.contrib.auth import get_user_model
User = get_user_model()


def signup_coach(request):
    form = UserCreationForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user.user_role = User.UserRole.COACH
            user.save()
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    return render(request, 'signup.html', {'form': form})
