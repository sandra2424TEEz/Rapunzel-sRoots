
# from django.contrib.auth.models import User
# from django.db import models
# from django.utils.timezone import now

# class UserProfile(models.Model):
#     ROLE_CHOICES = [
#         ('admin', 'Admin'),
#         ('brand', 'Brand'),
#         ('user', 'User'),
#     ]

#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')  # New field for roles
#     preferences = models.CharField(max_length=255, blank=True, null=True)

#     def __str__(self):
#         return f"{self.user.username} ({self.role})"

#     def get_preferences_list(self):
#         """Returns preferences as a list, assuming they are comma-separated."""
#         return self.preferences.split(',') if self.preferences else []

#     def set_preferences(self, preferences_list):
#         """Sets preferences by converting a list to a comma-separated string."""
#         self.preferences = ','.join(preferences_list)
#         self.save()


# class Product(models.Model):
#     CATEGORY_CHOICES = [
#         ('dandruff', 'Dandruff Solutions'),
#         ('hair_fall', 'Hair Fall Control'),
#         ('volumizing', 'Volumizing Products'),
#         ('nourishment', 'Nourishment Oils'),
#     ]

#     name = models.CharField(max_length=200)
#     description = models.TextField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
#     image = models.ImageField(upload_to='products/images/')
#     stock = models.PositiveIntegerField(default=10)  # New stock field

#     def __str__(self):
#         return self.name

#     def is_in_stock(self):
#         """Returns whether the product is in stock."""
#         return self.stock > 0

#     def update_stock(self, quantity):
#         """Update stock after purchase or cart addition."""
#         if quantity > self.stock:
#             raise ValueError("Not enough stock available!")
#         self.stock -= quantity
#         self.save()


# class CartItem(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
#     added_at = models.DateTimeField(default=now)

#     def save(self, *args, **kwargs):
#         """Ensure stock is available before saving"""
#         if self.quantity > self.product.stock:
#             raise ValueError("Not enough stock available!")
#         # Update stock of the product when added to cart
#         self.product.update_stock(self.quantity)
#         super().save(*args, **kwargs)

#     def total_price(self):
#         """Returns the total price of the cart item."""
#         return self.quantity * self.product.price

#     def __str__(self):
#         return f'{self.product.name} - {self.quantity} item(s)'


# class ShopkeeperRequest(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     product_name = models.CharField(max_length=100)
#     product_description = models.TextField()
#     product_category = models.CharField(max_length=50)
#     product_price = models.DecimalField(max_digits=10, decimal_places=2)
#     product_image = models.ImageField(upload_to='shopkeeper_requests/')
#     approved = models.BooleanField(default=False)
#     date_requested = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ('user', 'product_name')  # Prevent duplicate product requests

#     def __str__(self):
#         return f'Request for {self.product_name} by {self.user.username}'
from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('shopkeeper', 'Shopkeeper'),
        ('user', 'User'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='user')
    preferences = models.CharField(max_length=255, blank=True, default="")

    def __str__(self):
        return f"{self.user.username} ({self.role})"

    def get_preferences_list(self):
        return [p.strip() for p in self.preferences.split(',')] if self.preferences else []

    def set_preferences(self, preferences_list):
        self.preferences = ','.join(p.strip() for p in preferences_list if p.strip())
        self.save()
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('dandruff', 'Dandruff Solutions'),
        ('hair_fall', 'Hair Fall Control'),
        ('volumizing', 'Volumizing Products'),
        ('nourishment', 'Nourishment Oils'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='products/images/')
    stock = models.PositiveIntegerField(default=10)

    def __str__(self):
        return self.name

    def is_in_stock(self):
        return self.stock > 0

    def update_stock(self, quantity):
        if quantity > self.stock:
            raise ValueError("Not enough stock available!")
        self.stock -= quantity
        self.save()


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(default=now)

    def save(self, *args, **kwargs):
        if self.quantity > self.product.stock:
            raise ValueError("Not enough stock available!")
        self.product.update_stock(self.quantity)
        super().save(*args, **kwargs)

    def total_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f'{self.product.name} - {self.quantity} item(s)'


class ShopkeeperRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    product_description = models.TextField()
    product_category = models.CharField(max_length=50)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_image = models.ImageField(upload_to='shopkeeper_requests/')
    approved = models.BooleanField(default=False)
    date_requested = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product_name')

    def __str__(self):
        return f'Request for {self.product_name} by {self.user.username}'
