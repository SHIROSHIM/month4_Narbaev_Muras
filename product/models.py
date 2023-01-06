from django.db import models
from .models import Product
# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=50)


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.IntegerField(max_length=7)
    category = models.ManyToManyField(Category)


class Review(models.Model):
    products = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    text = models.TextField()
    created_date = models.DateField(auto_now=True)
    rate = models.FloatField()


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price']


class ReviewCreateForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['product', 'title', 'review', 'rating']
