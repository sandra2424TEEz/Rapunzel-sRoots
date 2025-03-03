# # Register your models here.
# from django.contrib import admin

# from .models import Product

# # Define a custom admin interface for the Product model
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('name', 'price', 'description', 'image')  # Fields to display in the list view
#     search_fields = ('name', 'description')  # Fields you can search by in the admin
#     list_filter = ('price',)  # Filter products by price in the admin
#     ordering = ('-price',)  # Default ordering of the products, sorted by price in descending order

#     # Optional: Allow editing products directly in the list view (inline editing)
#     # list_editable = ('price', 'description')  # This would make price and description editable directly in the list view

# # Register the Product model with the custom admin configuration
# admin.site.register(Product, ProductAdmin)

# from django.contrib import admin
# from .models import Product, UserProfile, CartItem
# from .models import Cart

# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('name', 'price', 'category', 'stock', 'description', 'image')
#     search_fields = ('name', 'description', 'category')
#     list_filter = ('category', 'price')
#     ordering = ('-price',)
#     list_editable = ('price', 'stock')

# @admin.register(UserProfile)
# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'preferences')
#     search_fields = ('user__username', 'preferences')

# @admin.register(CartItem)
# class CartItemAdmin(admin.ModelAdmin):
#     list_display = ('user', 'product', 'quantity')
#     search_fields = ('user__username', 'product__name')
#     list_filter = ('user', 'product')
#     ordering = ('user', 'product')
# admin.site.register(Cart)

from django.contrib import admin
from .models import Product, UserProfile, CartItem, ShopkeeperRequest

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'stock', 'description', 'image')
    search_fields = ('name', 'description', 'category')
    list_filter = ('category', 'price')
    ordering = ('-price',)
    list_editable = ('price', 'stock')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'preferences')
    search_fields = ('user__username', 'preferences')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'added_at')
    search_fields = ('user__username', 'product__name')
    list_filter = ('user', 'product')
    ordering = ('user', 'product')

@admin.register(ShopkeeperRequest)
class ShopkeeperRequestAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'user', 'product_category', 'product_price', 'approved', 'date_requested')
    list_filter = ('approved', 'product_category', 'date_requested')
    search_fields = ('product_name', 'user__username', 'product_category')
    actions = ['approve_selected_requests']

    def approve_selected_requests(self, request, queryset):
        """Action to approve selected requests"""
        queryset.update(approved=True)
        self.message_user(request, "Selected requests have been approved.")
    
    approve_selected_requests.short_description = "Approve selected requests"

