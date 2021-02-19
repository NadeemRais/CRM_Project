from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
	user= models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	phone = models.BigIntegerField(null=True)
	email = models.EmailField(max_length=200, null=True)
	profile_pic = models.ImageField(default="profile1.png", null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.name


class Tag(models.Model):
	name = models.CharField(max_length=200)

	def __str__(self):
		return self.name




class Product(models.Model):

	CATEGORY=(

		('Indoor','Indoor'),
		('Outdoor', 'Outdoor'),

		)


	name = models.CharField(max_length=200, null=True)
	price = models.FloatField(max_length=200, null=True)
	category = models.CharField(max_length=200, null=True, choices=CATEGORY)
	description = models.CharField(max_length=200, null=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	Tag = models.ManyToManyField(Tag)

	def __str__(self):
		return self.name






class Order(models.Model):
	STATUS=(

			('Panding','Panding'),
			('Out of delivery', 'Out of delivery'),
			('Delivered', 'Delivered')

		)

	customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
	product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	status=models.CharField(max_length=200, null=True, choices=STATUS)
	note =models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.product.name
	
