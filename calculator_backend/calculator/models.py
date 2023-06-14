from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Permission

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('user_balance', 10.0)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('user_balance', 10.0)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class CustomUser(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, blank=True, null=True)
    user_balance = models.DecimalField(max_digits=10, decimal_places=2, default=10.0, null=True, blank=True)
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    
    objects = CustomUserManager()

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='customuser_set',
        help_text='The permissions this user has',
        related_query_name='user',
    )
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email

class Operation(models.Model):
    OPERATION_CHOICES = [
        ('addition', 'Addition'),
        ('subtraction', 'Subtraction'),
        ('multiplication', 'Multiplication'),
        ('division', 'Division'),
        ('square_root', 'Square Root'),
        ('random_string', 'Random String'),
    ]
    type = models.CharField(max_length=15, choices=OPERATION_CHOICES)
    cost = models.FloatField()

class Record(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    operation_response = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def serialize(self):
        serialized_data = {
            'id': self.id,
            'operation': {
                'id': self.operation.id,
                'type': self.operation.type,
                'cost': self.operation.cost,
            },
            'amount': self.amount,
            'operation_response': self.operation_response,
            'date': self.date,
        }
        return serialized_data
