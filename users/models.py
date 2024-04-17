from django.db import models

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=100)
    pan = models.CharField(max_length=10,default='')
    email = models.EmailField()
    address = models.TextField()

    def __str__(self):
        return self.name

class Otp(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.email)

    def is_expired(self):
        expiration_time = self.date + timezone.timedelta(minutes=3)
        return timezone.now() > expiration_time