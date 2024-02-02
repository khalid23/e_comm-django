from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Collection(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='collection_images/')

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    details = models.TextField()
    sizes = models.TextField()
    quantity = models.PositiveIntegerField(default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    is_featured = models.BooleanField(default=False)
    colors = models.ManyToManyField(Color, related_name='products')
    collections = models.ManyToManyField(Collection, related_name='products')
    is_new_arrival = models.BooleanField(default=False)
    is_sold_out = models.BooleanField(default=False)
    discount_percentage = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')
