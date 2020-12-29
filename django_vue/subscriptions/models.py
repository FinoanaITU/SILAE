from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class Posts(models.Model):

    title = models.CharField(max_length=250)
    content = models.TextField()

    def __str__(self):
        return self.title

class MyUtilisateurManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("l'utilisateur doit avoir un email")
        if not username:
            raise ValueError("l'utilisateur doit avoir un nom d'utilisateur")

        user = self.model(
            email=self.normalize_email(email),
            username=username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password = password,
            username = username
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
class Utilisateur(AbstractBaseUser):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True) 
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False) 
    is_active = models.BooleanField(default=True) 
    is_staff = models.BooleanField(default=False) 
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    objects = MyUtilisateurManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True