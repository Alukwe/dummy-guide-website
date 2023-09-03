from django.db import models

# Create your models here.

class Categories(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    # parent_category = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"
#
# class User(models.Model):
#     name = models.CharField(max_length=100)
#     image = models.ImageField()

# class Subcategory(models.Model):
#     name = models.CharField(max_length=100)
#     category = models.ForeignKey(Categories, on_delete=models.CASCADE)
class Services(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE) # many_to_many relationship
    # subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, null=True, blank=True)
    # video_ulr = models.URLField(null=True, blank=True)
    # client = models.ManyToManyField(User, through='Booking') #

    def __str__(self):
        return f'{self.name}'

class ServiceImages(models.Model):
    service = models.ForeignKey(Services, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/service_images/')

# class Booking(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     service = models.ForeignKey(Services, on_delete=models.CASCADE)
#     booking_date = models.DateTimeField(auto_now_add=True)
#

# class Order(models.Model):
#     service = models.ForeignKey(Services, on_delete=models.CASCADE) # many_to_many relationship
#     # user = models.ForeignKey(User, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()
#     total_price = models.DecimalField(max_length=10, decimal_places=2)
#     order_date =models.DateTimeField(auto_now_add=True)

# class Reviews(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     service = models.ForeignKey(Services, on_delete=models.CASCADE)
#     rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
#     comment = models.TextField()
#     review_date = models.DateTimeField(auto_now_add=True)
