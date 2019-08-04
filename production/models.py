from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db.models.signals import post_save

from django.utils import timezone

class ProUserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Please input an email.')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        user=self.create_user(email, name, password)
        user.is_staff = True
        user.is_superuser= True
        user.set_password(password)
        user.save(using=self._db)

        return user


class ProUser(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)
    
    objects = ProUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name
    
    def __str__(self):
        return self.email

class Production(models.Model):
    user = models.ForeignKey(ProUser,
                             on_delete = models.CASCADE,
                             primary_key= False,)
    machine = models.CharField(max_length=50)
    shift = models.TextField()
    job = models.TextField()
    quantity = models.TextField()
    date = models.DateField(auto_now_add=False)
    in_question = models.BooleanField(default = False)
    def __str__(self):
        return self.machine
    class Meta:
        verbose_name_plural = "Production Lots"

class Machine(models.Model):
    user = models.ForeignKey(ProUser,
                             on_delete = models.CASCADE)
    machine = models.CharField(max_length=50)
    current_job = models.TextField(max_length=50, null=True, default="")
    def __str__(self):
        return self.machine
    class Meta:
        verbose_name_plural = "Machines"
        unique_together = (('user', 'machine'),)

class StartTime(models.Model):
    user = models.ForeignKey(ProUser,
                             on_delete = models.CASCADE)
    machine = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=False)
    time = models.TimeField(auto_now_add=False)
    def __str__(self):
        return self.machine
    class Meta:
        verbose_name_plural = "Starting Times"

class Part(models.Model):
    user = models.ForeignKey(ProUser,
                             on_delete = models.CASCADE)
    part = models.TextField(max_length=50)
    job = models.CharField(max_length=20)
    machine = models.CharField(max_length=50)
    order_quantity = models.TextField(max_length=10, null=True, default=None)
    possible_quantity = models.TextField(max_length=10, null=True, default=None)
    remaining_quantity = models.TextField(max_length=10, null=True, default=None)
    weight_recieved = models.TextField(max_length=10, null=True, default=None)
    weight_length = models.TextField(max_length=10, null=True, default=None)
    weight_quantity = models.TextField(max_length=10, null=True, default=None)
    oal = models.TextField(max_length=10, null=True, default=None)
    cut_off = models.TextField(max_length=10, null=True, default=None)
    main_facing = models.TextField(max_length=10, null=True, default=None)
    sub_facing = models.TextField(max_length=10, null=True, default=None)
    heat_lot = models.TextField(max_length=30, null=True, default=None)
    cycle_time = models.TextField(max_length=10, null=True, default=None)
    bars = models.TextField(max_length=250, null=True, default=None)
    def __str__(self):
        return self.part
    class Meta:
        verbose_name_plural = "Parts"
        unique_together = (('machine', 'job'),)

class HourlyProduction(models.Model):
    user = models.ForeignKey(ProUser,
                             on_delete = models.CASCADE)
    machine = models.CharField(max_length=200)
    hard_quantity = models.TextField(max_length=200, default='0')
    counter_quantity = models.TextField(max_length=200, null=True, default='')
    job = models.TextField(max_length=50, null=True, default="")
    time = models.TimeField(auto_now_add=False)
    date = models.DateField(auto_now_add=False)
    def __str__(self):
        return self.hard_quantity
    class Meta:
        verbose_name_plural = "Statuses"

class ChangeLog(models.Model):
    user = models.ForeignKey(ProUser,
                            on_delete = models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    old_values = models.TextField(max_length=2000)
    change_type = models.CharField(max_length=50)
    changed_model = models.TextField(max_length=20)
    changed_id = models.TextField(max_length=20)
    def __str__(self):
        return self.old_values
    class Meta:
        verbose_name_plural = "Logged Changes"