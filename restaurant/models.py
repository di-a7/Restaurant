from django.db import models
from account.models import *
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from datetime import time
from django.utils import timezone
# from django.contrib.auth import get_user_model

# Create your models here.

class Menu(models.Model):
	CATEGORY_CHOICES = [
		('appetizer', 'Appetizer'),
		('breakfast', 'Breakfast'),
		('salads', 'Salads'),
		('main', 'Main'),
		('dessert', 'Dessert'),
		('drink', 'Drink'),
		('side_dish', 'Side Dish'),
	]
	name = models.CharField(max_length=50)
	category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
	description = models.TextField()
	price = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return self.name

class Table(models.Model):
	STATUS_CHOICES=[
		('available','Available'),
		('occupied','Occupied'),
		('reserved','Reserved'),
	]
	table_number = models.IntegerField(unique=True)
	capacity=models.IntegerField()
	status = models.CharField(max_length=20, choices= STATUS_CHOICES, default='available')

	def __str__(self):
		return f"Table {self.table_number}"

class Order(models.Model):
	STATUS_CHOICES = [
		('received', 'Received'),
		('preparation', 'In Preparation'),
		('ready', 'Ready for Delivery/Pickup'),
		('delivered', 'Delivered'),
	]
	ORDER_TYPE_CHOICES=[
		('dine-in','Dine-In'),
		('takeout','Takeout'),
		('delivery','Delivery'),
	]
	user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
	order_type = models.CharField(max_length=20, choices=ORDER_TYPE_CHOICES)
	table=models.ForeignKey(Table,on_delete=models.CASCADE, null=True, blank=True)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='received')
	# created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Order {self.id} ({self.get_status_display()})"
	
class OrderItem(models.Model):
	order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
	menu = models.ForeignKey('Menu', on_delete=models.CASCADE)
	quantity = models.IntegerField(default=1)
	special_requests = models.TextField(blank=True, null=True)

	def __str__(self):
		return f"{self.quantity}x {self.menu.name} - {self.order}"
	
class Kitchen(models.Model):
	STATUS_CHOICES = [
		('pending', 'Pending'),
		('prepared', 'Prepared'),
		('served', 'Served'),
	]
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='kitchen')
	preparation_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
	
	def __str__(self):
		return f"Kitchen Order #{self.id} ({self.preparation_status})"
	
class Bill(models.Model):
	order = models.OneToOneField(Order, on_delete = models.CASCADE, related_name='bill')
	generated_by = models.ForeignKey(User, on_delete=models.CASCADE)
	generated_at = models.DateTimeField(auto_now_add = True)
	def __str__(self):
		return f"Bill for Order #{self.order.id}"

class Ingredient(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name

class InventoryItem(models.Model):
	ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
	quantity = models.DecimalField(max_digits=10, decimal_places=2)
	unit_of_measurement = models.CharField(max_length=50)
	used_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True,blank=True)
	expiration_date = models.DateField()

	def save(self, *args, **kwargs):
		if self.used_quantity is not None and self.used_quantity > self.quantity:
			raise ValidationError("Used quantity cannot exceed total quantity.")
		super().save(*args, **kwargs)
      
	def __str__(self):
		return f"{self.ingredient.name} - {self.used_quantity}/{self.quantity}{self.unit_of_measurement} {self.ingredient}"