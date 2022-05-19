from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
# from taggit.managers import TaggableManager


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **other_fields):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            **other_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **other_fields):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            role='admin',
            **other_fields
        )
        # user.admin = True
        user.save(using=self._db)
        return user


class Skills(models.Model):
    name = models.SlugField()
    objects = models.Manager()

    class Meta:
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'

    def __str__(self):
        return f'{self.name}'


class User(AbstractBaseUser):
    user = "user"
    moderator = "moderator"
    admin = "admin"
    ROLE = [
        (user, 'user'),
        (moderator, 'moderator'),
        (admin, 'admin')
    ]
    first_name = models.CharField(max_length=20, default='Unknown')
    last_name = models.CharField(max_length=20, default='Unknown')
    role = models.CharField(max_length=10, default='user', choices=ROLE, null=True)
    # tags = TaggableManager()
    skills = models.ManyToManyField(Skills, default='Unknown')
    email = models.EmailField(blank=True, null=True, unique=True)
    hobby = models.CharField(max_length=20, default='Unknown')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ("id",)

    # эта константа определяет поле для логина пользователя
    USERNAME_FIELD = 'email'

    # также для работы модели пользователя должен быть переопределен
    # менеджер объектов
    objects = MyUserManager()

    # эта константа содержит список с полями,
    # которые необходимо заполнить при создании пользователя
    REQUIRED_FIELDS = ['hobby']

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def is_admin(self):
        return self.role == self.admin

    @property
    def is_user(self):
        return self.role == self.user



