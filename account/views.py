from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login

from .forms import LoginForm


# Пример Обработчика Логина
def user_login(request):
    print(request.body)
    if request.method == 'POST':
        # Создаем объект формы
        form = LoginForm(request.POST)
        # Валидируем
        if form.is_valid():
            cd = form.cleaned_data
            # Сверяем с базой данных. Функция возвращает обьект User,
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            # если он успешно аутентифицирован
            if user is not None:
                if user.is_active:
                    # сохраняет текушего пользователя в сессии
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disable account')
            else:
                return HttpResponse('Invalid login and password')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})
