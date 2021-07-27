"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

import rest_framework
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import SimpleRouter

from apps.users.views import UserViewSet, PermissionViewSet, RoleViewSet
from apps.customers.views import CustomerViewSet
from apps.products.views import ProductViewSet, CategoryViewSet, ProductImageViewSet
from apps.checkouts.views import CartViewSet, CartItemViewSet, OrderViewSet, OrderItemViewSet

swagger_info = openapi.Info(
    title="Eureka API",
    default_version="v1",
    description="""Eureka project.""",
    contact=openapi.Contact(email="hr@ftech.ai"),
    license=openapi.License(name="Private"),
)

schema_view = get_schema_view(
    info=swagger_info,
    public=True,
    authentication_classes=[
        rest_framework.authentication.SessionAuthentication
    ],
    permission_classes=[permissions.IsAdminUser],
)

api_router = SimpleRouter(trailing_slash=False)

# users
api_router.register("users", UserViewSet, basename="users")
# ---------
# customers
api_router.register("customers", CustomerViewSet, basename="customers")
# ---------
api_router.register('permissions', PermissionViewSet, basename='permissions')
# roles
api_router.register('roles', RoleViewSet, basename='roles')
# ---------
# category
api_router.register('categories', CategoryViewSet, basename='categories')
# ---------
# products
api_router.register('products', ProductViewSet, basename='products')
# ---------
# product_images
api_router.register('product_images', ProductImageViewSet, basename='product_images')
# ---------
# carts
api_router.register('carts', CartViewSet, basename='carts')
# ---------
# cart_items
api_router.register('cart_items', CartItemViewSet, basename='cart_items')
# ---------
# orders
api_router.register('orders', OrderViewSet, basename='orders')
# ---------
# order_items
api_router.register('order_items', OrderItemViewSet, basename='order_items')
# ---------
admin.autodiscover()

urlpatterns = [
    path("admin/", admin.site.urls),
    path(r"api/v1/", include(api_router.urls)),
]

urlpatterns.extend([
    path(
        r"swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
])
