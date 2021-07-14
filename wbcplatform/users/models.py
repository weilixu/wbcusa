from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.templatetags.static import static


def user_directory_path(instance, filename):
    return 'profile_img/{0}/{1}'.format(instance.user.id, filename)


class Profile(models.Model):
    GENDER_MALE = 1
    GENDER_FEMALE = 2
    GENDER_CHOICES = [
        (GENDER_MALE, _("Male")),
        (GENDER_FEMALE, _("Female")),
    ]

    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES, null=True, blank=True)
    phone = models.CharField(max_length=32, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    number = models.CharField(max_length=32, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    zip = models.CharField(max_length=30, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profile')

    @property
    def get_avatar(self):
        return self.avatar.url if self.avatar else static('img/profile_small.jpg')