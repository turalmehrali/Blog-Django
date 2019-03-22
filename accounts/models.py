
from django.db import models
from django.contrib.auth.models import User


class UserType(models.Model):

    user_type = models.CharField(max_length=20, default='simple_user', verbose_name='Hesab növü')

    def __str__(self):
        return self.user_type

    class Meta:
        verbose_name_plural = 'Hesab növləri'
        verbose_name = 'Hesab növü'


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='İstifadəçi')
    bio = models.TextField(max_length=2000, blank=True, verbose_name='Bioqrafiya')
    profile_photo = models.ImageField(upload_to='media', default='default.png', blank=True, verbose_name='Profil rəsmi')
    user_type = models.ForeignKey(UserType, default=2, on_delete=models.CASCADE, null=True, verbose_name='Hesab növü')

    def __str__(self):
        return self.user.username


    class Meta:
        verbose_name_plural = 'Profillər'
        verbose_name = 'Profil'


