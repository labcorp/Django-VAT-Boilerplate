from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from apps.core.utils.shortcuts import rand_string
from apps.core.models import AbstractBaseModel


class User(AbstractBaseModel, AbstractUser):
    email = models.EmailField(_('email address'), unique=True, null=True)

    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'

    @property
    def display_name(self):
        return self.get_full_name() or self.username

    def __str__(self):
        return self.display_name


def user_avatar_path(instance, filename):
    return f'users/avatars/{instance.user.pk}/{filename}'


class Profile(AbstractBaseModel):
    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    key = models.CharField(_('pix key'), max_length=128, blank=True)
    nickname = models.CharField(_('nickname'), max_length=64)
    doc = models.CharField(_('CPF'), max_length=16, blank=True)
    avatar = models.ImageField(_('avatar'), upload_to=user_avatar_path, null=True, blank=True, validators=[FileExtensionValidator(['gif', 'png', 'jpg', 'jpeg'])])
    birth_date = models.DateField(_('birthdate'), null=True, blank=True)
    optin = models.BooleanField(_('opt-out'), default=False)

    def save(self, *args, **kwargs):
        other = Profile.objects.filter(nickname=self.nickname).exclude(pk=self.pk)
        if other.count():
            self.nickname = f'{self.nickname}-{rand_string()}'

        super().save()

    def __str__(self):
        return self.user.display_name
