from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission

class MyUserManager(BaseUserManager):
    def create_user(self, student_id, password=None, **extra_fields):
        if not student_id:
            raise ValueError('The Student ID must be set')
        user = self.model(student_id=student_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, student_id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        # Ensure the values of is_staff and is_superuser are True
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(student_id, password, **extra_fields)

class MyUser(AbstractBaseUser, PermissionsMixin):
    LEVEL_CHOICES = [
        ('1', 'ชั้นปีที่ 1'),
        ('2', 'ชั้นปีที่ 2'),
        ('3', 'ชั้นปีที่ 3'),
        ('4', 'ชั้นปีที่ 4'),
    ]
    
    student_id = models.CharField(max_length=11, unique=True, primary_key=True)
    level = models.CharField(max_length=1, choices=LEVEL_CHOICES, default='1')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'student_id'
    REQUIRED_FIELDS = ['level']

    def __str__(self):
        return self.student_id

class ValidStudentID(models.Model):
    student_id = models.CharField(max_length=11, unique=True)

    def __str__(self):
        return self.student_id

class AdminUserManager(BaseUserManager):
    def create_admin(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Admins must have an email address')
        email = self.normalize_email(email)
        admin = self.model(email=email, **extra_fields)
        admin.set_password(password)
        admin.save(using=self._db)
        return admin

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_admin(email, password, **extra_fields)

class AdminUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    # Explicitly declare groups and user_permissions with unique related_names
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="admin_user_set",
        related_query_name="admin_user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="admin_user_set",
        related_query_name="admin_user",
    )

    objects = AdminUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email