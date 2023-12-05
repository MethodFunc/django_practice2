from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import SignupForm, ProfileForm, PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.views import (LoginView, logout_then_login, PasswordChangeView as AuthPasswordChange)
from django.contrib.auth import login as auth_login
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy

# Create your views here.
# def login(request):
#     pass
#     # return render(request, 'accounts/login.html')
login = LoginView.as_view(template_name='accounts/login_form.html')


def logout(request):
    messages.success(request, "Logout success")
    # 로그아웃 시 자동으로 로그인 페이지로 이동
    return logout_then_login(request)


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            signed_user = form.save()
            # 회원 가입 후 자동 로그인 처리
            auth_login(request, signed_user)

            messages.success(request, 'Account created successfully')

            # 이메일 보내는 처리
            signed_user.send_welcome_email()  # Todo: Fixed: Celery처리 및 비동기 처리
            next_url = request.GET.get("next", "/")
            return redirect(next_url)
    else:
        form = SignupForm()

    return render(request, 'accounts/signup_form.html', {'form': form})


@login_required
def profile_edit(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile_edit')
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'accounts/profile_edit_form.html', {
        "form": form
    })


# @login_required
# def password_change(request):
#     pass
#     # return render(request, 'accounts/password_change_form.html.html')


class PasswordChangeView(LoginRequiredMixin, AuthPasswordChange):
    success_url = reverse_lazy('password_change')
    template_name = 'accounts/password_change_form.html'
    form_class = PasswordChangeForm

    def form_valid(self, form):
        messages.success(self.request, 'Password changed successfully')
        return super().form_valid(form)


password_change = PasswordChangeView.as_view()
