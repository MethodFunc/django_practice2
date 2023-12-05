from .models import User
from django import forms
from django.contrib.auth.forms import (UserCreationForm, PasswordChangeForm as AuthPasswordChangeForm)


class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 필수 등록 여부 설정
        self.fields["email"].required = True
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "email", "first_name", "last_name"]

    # 이메일 유효성 검사
    def clean_email(self):
        email = self.cleaned_data.get("email")

        if email:
            qs = User.objects.filter(email=email)
            if qs.exists():
                raise forms.ValidationError("Email already exists")
        return email


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["profile", "last_name", "first_name", "gender", "email", "phone_number", "bio"]


class PasswordChangeForm(AuthPasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["old_password"].widget.attrs["placeholder"] = "Current Password"
        self.fields["new_password1"].widget.attrs["placeholder"] = "New Password"
        self.fields["new_password2"].widget.attrs["placeholder"] = "Confirm New Password"

    def clean_new_password2(self):
        new_password2 = super().clean_new_password2()
        old_password = self.cleaned_data.get("old_password")
        if old_password and new_password2:
            if old_password == new_password2:
                raise forms.ValidationError("Passwords cannot be the same")
        return new_password2

# class PasswordChangeForm(forms.Form):
#     current_password = forms.CharField(widget=forms.PasswordInput)
#     new_password = forms.CharField(widget=forms.PasswordInput)
#     new_password_check = forms.CharField(widget=forms.PasswordInput)
#
#     # 비밀번호 일치 여부 검사
#     def clean(self):
#         cleaned_data = super().clean()
#         new_password = cleaned_data.get("new_password")
#         new_password_check = cleaned_data.get("new_password_check")
#
#         if new_password != new_password_check:
#             self.add_error("new_password_check", "Passwords do not match")
#         return cleaned_data
#
#     # 비밀번호 길이 검사
#     def clean_new_password(self):
#         new_password = self.cleaned_data.get("new_password")
#         if len(new_password) < 8:
#             self.add_error("new_password", "Password must be at least 8 characters long")
#         return new_password
#
#     # 현재 비밀번호 검사
#     def clean_current_password(self):
#         current_password = self.cleaned_data.get("current_password")
#         user = self.user
#         if not user.check_password(current_password):
#             self.add_error("current_password", "Incorrect password")
#         return current_password
