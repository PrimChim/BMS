from django.db import models

# Create your models here.
class Items(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    description = models.TextField()

    def __str__(self):
        return self.name

# bill details model
class Bills(models.Model):
    bill_no = models.IntegerField(default=1, editable=True)

    customer_id = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    invoice_date = models.DateTimeField()
    status = models.CharField(max_length=10, default='regular', choices=[('regular', 'regular'), ('cancelled', 'cancelled')])
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)


    def __str__(self):
        return str(self.id)

# bill items details model
class BillItems(models.Model):
    bill = models.ForeignKey(Bills, on_delete=models.CASCADE)
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return str(self.bill_id)

# business details
class Business(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    website = models.URLField()

    def __str__(self):
        return self.name