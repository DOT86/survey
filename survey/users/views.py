from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.views import View

class LoginView(View):
    """Представление для входа пользователя"""

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('quiz_list')

        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                next_url = request.POST.get('next') or request.GET.get('next') or 'quiz_list'

                messages.success(request, f'Добро пожаловать, {user.username}!')
                return redirect(next_url)

        # Если форма не валидна
        messages.error(request, 'Неверное имя пользователя или пароль.')
        return render(request, 'registration/login.html', {'form': form})