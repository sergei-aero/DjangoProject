from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.core.mail import send_mail
from django.conf import settings
from .forms import UserRegisterForm, UserLoginForm, ProfileForm
from .models import User

class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        # Сохраняем пользователя (password хешируется в форме)
        user = form.save()
        # Автоматически логиним после регистрации
        login(self.request, user)
        # Отправляем письмо
        send_mail(
            subject='Добро пожаловать!',
            message=f'{user.email}, вы успешно зарегистрировались на Skystore.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )
        return super().form_valid(form)

class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'
    next_page = reverse_lazy('catalog:product_list')

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('catalog:product_list')

    def get_object(self, queryset=None):
        return self.request.user   # редактируем текущего пользователя
