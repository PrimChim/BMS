from django.db import models

# Create your models here.
class Items(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return self.name

# bill details model
class Bills(models.Model):
    customer_id = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    invoice_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

# bill items details model
class BillItems(models.Model):
    bill = models.ForeignKey(Bills, on_delete=models.CASCADE)
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return str(self.bill_id)