from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from django.shortcuts import resolve_url

from django.template.loader import render_to_string
from django.contrib.auth import get_user_model


# Create your models here.

class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"
        OTHER = "O", "something that's not a man or a woman"

    follower_set = models.ManyToManyField("self", blank=True)
    following_set = models.ManyToManyField("self", blank=True)

    website_url = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    phone_number = models.CharField(
        validators=[RegexValidator(r"^010-?\d{4}-?\d{4}$")], max_length=13, blank=True)
    gender = models.CharField(choices=GenderChoices.choices, max_length=10, blank=True)
    profile = models.ImageField(blank=True, upload_to="accounts/profile/%Y/%m/%d",
                                help_text="48 px * 48 px png/jpg")

    # phone = models.CharField(max_length=20, blank=True)
    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def avatar(self):
        if self.profile:
            return self.profile.url
        else:
            return resolve_url("pydenticon_image", self.username)

    def send_welcome_email(self):
        subject = render_to_string("accounts/welcome_email_subject.txt",
                                   {"user": self})
        content = render_to_string("accounts/welcome_email_content.txt",
                                   {"user": self})
        sender_email = settings.EMAIL_HOST_USER
        send_mail(subject=subject, message=content, from_email=sender_email,
                  recipient_list=[self.email], fail_silently=False)

        # def save(self, *args, **kwargs):
        #     is_created = self.pk == None
        #     super().save(*args, **kwargs)

        # ... email logic

        return self.username
