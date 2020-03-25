from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, user_code, username, password):
        if not user_code:
            raise ValueError('Users must have an usercode')

        user = self.model(
            user_code=user_code,
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_code, username, password, gender):
        user = self.create_user(
            user_code=user_code,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = [
        (1, '男'),
        (2, '女'),
    ]
    user_code = models.CharField(max_length=10, verbose_name='柜员号', unique=True)
    username = models.CharField(max_length=50, verbose_name='用户名')
    gender = models.IntegerField(choices=GENDER_CHOICES, default=1, verbose_name='性别')
    is_active = models.BooleanField(default=True, verbose_name='是否激活')
    is_admin = models.BooleanField(default=False, verbose_name='是否允许访问管理界面')

    USERNAME_FIELD = 'user_code'
    REQUIRED_FIELDS = ['username', 'gender']

    objects = UserManager()

    class Meta:
        verbose_name_plural = '用户'

    def get_full_name(self):
        return self.user_code

    def get_short_name(self):
        return self.username

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_admin
