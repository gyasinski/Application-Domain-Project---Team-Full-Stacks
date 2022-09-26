from locale import normalize
from tokenize import blank_re
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, AbstractBaseUser




class UserManager(BaseUserManager):
    def create_user(self, email, username, employee_id, password=None):
        if not email:
            raise ValueError("Users must have a valid email address")
        if not username:
            raise ValueError("Users must have a valid username")
        if not employee_id:
            raise ValueError("Users must have a valid employee id")

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            employee_id = employee_id,
        )

        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, email, username, employee_id, password=None):

        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            employee_id = employee_id,
        ) 

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.set_password(password)
        user.save(using=self.db)

        return user




class User(AbstractBaseUser):
    employee_id             = models.IntegerField(primary_key=True, unique=True)
    user_role               = models.CharField(max_length=50)
    email                   = models.EmailField(verbose_name="email", max_length=50, null=True)
    username                = models.CharField(max_length=50, unique=True)
    first_name              = models.CharField(max_length=50)
    last_name               = models.CharField(max_length=50)
    password                = models.CharField(max_length=50)
    password_init_dt        = models.DateTimeField(auto_now_add=True)
    date_of_birth           = models.DateField(null=True)
    is_active               = models.BooleanField(default=True)
    is_admin                = models.BooleanField(default=False)
    is_mgr                  = models.BooleanField(default=False)
    is_accountant           = models.BooleanField(default=False)
    is_staff                = models.BooleanField(default=False)
    is_superuser            = models.BooleanField(default=False)
    # profile_image           = models.ImageField(max_length=255, upload_to=, null=True, blank=True, default=) TO DO: Add image functionality

    objects = UserManager()

    USERNAME_FIELD = 'employee_id'
    REQUIRED_FIELDS = ['username']

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def get_username(self):
        return self.username
    
    def get_email(self):
        return self.email

    def get_first_name(self):
        return self.first_name

    def get_password(self):
        return self.password


    def __str__(self):
        return self.username