import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, name, annual_income, aadhar_id, password, **extra_fields):
        if not email:
            raise ValueError("User must have an email address")
        if not name:
            raise ValueError("User must have a name")
        if not annual_income:
            raise ValueError("User must have an annual income")
        if not aadhar_id:
            raise ValueError("User must have an aadhar id")

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            annual_income=annual_income,
            aadhar_id=aadhar_id,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, annual_income, aadhar_id, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(
            email=self.normalize_email(email),
            name=name,
            annual_income=annual_income,
            aadhar_id=aadhar_id,
            **extra_fields
        )


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    annual_income = models.IntegerField(default=0)
    aadhar_id = models.UUIDField(
        default=uuid.uuid4, editable=True, unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'annual_income', 'aadhar_id']

    def __str__(self):
        return self.email


class CreditScore(models.Model):
    aadhar_id = models.OneToOneField('User', on_delete=models.CASCADE, unique=True, related_name='credit_score')
    credit_score = models.IntegerField(default=0)

    def __str__(self):
        return f"Credit Score of {self.aadhar_id} is {self.credit_score}"
    
    def get_credit_score(self):
        return self.credit_score
