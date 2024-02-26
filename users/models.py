from django.db import models

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=100)
    pan = models.CharField(max_length=10,default='')
    email = models.EmailField()
    address = models.TextField()

    def __str__(self):
        return self.name