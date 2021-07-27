from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem


class CartAdmin(admin.ModelAdmin):
    pass

admin.site.register(Cart, CartAdmin)

class CartItemAdmin(admin.ModelAdmin):
    pass

admin.site.register(CartItem, CartItemAdmin)

class OrderAdmin(admin.ModelAdmin):
    pass

admin.site.register(Order, OrderAdmin)

class OrderItemAdmin(admin.ModelAdmin):
    pass

admin.site.register(OrderItem, OrderItemAdmin)
