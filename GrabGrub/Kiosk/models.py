from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=300)
    password = models.CharField(max_length=300)
    objects = models.Manager()

    def getUsername(self):
        return self.username
    
    def getPassword(self):
        return self.password

    def __str__(self):
        return "Username: " + self.username + ", " + "Password: " + self.password

class Food(models.Model):
    name = models.CharField(max_length=300)
    description = models.CharField(max_length=300)
    price = models.FloatField()
    created_at = models.DateTimeField(blank=True, null=True)
    objects = models.Manager()

    def getName(self):
        return self.name

    def getDesc(self):
        return self.description

    def getPrice(self):
        return self.price

    def __str__(self):
        return str(self.pk) + ": " + self.name + " - " + str(self.price) + ", " + self.description + " created at: " + str(self.created_at)

class Customer(models.Model):
    name = models.CharField(max_length=300)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=300)
    objects = models.Manager()

    def getName(self):
        return self.name
    
    def getAddress(self):
        return self.address

    def getCity(self):
        return self.city

    def __str__(self):
        return str(self.pk) + ": " + self.name + " - " + self.address + ", " + self.city
    
class Order(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    qty = models.FloatField()
    ordered_at = models.DateTimeField(blank=True, null=True)
    cust_order = models.ForeignKey(Customer, on_delete=models.CASCADE)
    payment_mode = models.CharField(max_length=300)
    objects = models.Manager()

    def getMode(self):
        return self.payment_mode

    def getQuantity(self):
        return self.qty

    def __str__(self):
        return f"{self.pk}: Order {self.food.pk}: {self.food.getName()} ({self.qty}). For {self.cust_order.getName()}: {self.cust_order.getAddress()}, {self.cust_order.getCity()}. {self.payment_mode}, ordered at {self.ordered_at}"

