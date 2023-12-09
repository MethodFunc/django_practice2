from django.db import models
from accounts.models import User
from django.conf import settings

from django.urls import reverse
import re


class BaseModel(models.Model):
    create_dt = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# Create your models here.
"""
user
-> Post.objects.filter(author=user)
-> user.post_set.all()
"""


class Post(BaseModel):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="my_post_set")
    photo = models.ImageField(upload_to="instgram/post/%Y/%m/%d", )
    caption = models.CharField(max_length=500)
    tag_set = models.ManyToManyField("Tag", blank=True)
    location = models.CharField(max_length=100, blank=True)
    like_user_set = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="like_post_set")

    def __str__(self):
        return f"{self.author} - {self.caption}"

    def get_absolute_url(self):
        return reverse("instagram:post_detail", kwargs={"pk": self.pk})

    def extract_tag_list(self):
        pattern = r"#([a-zA-Z\dㄱ-힣]+)"
        tag_name_list = re.findall(pattern, self.caption)
        tag_list = []
        for tag_name in tag_name_list:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            tag_list.append(tag)

        return tag_list

    def is_like_user(self, user):
        return self.like_user_set.filter(pk=user.pk).exists()


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# # 2. 별도 모델 적용
# class LikePost(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
