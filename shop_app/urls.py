from django.urls import path , include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductListView,
    ProductDetailView,
    AddItemView,
    ProductInCartView,
    CartStartView,
    CartDetailView,
    UpdateQuantityView,
    DeleteCartItemView,
    UsernameView,
    UserInfoView
)


urlpatterns = [
    path("products/", ProductListView.as_view() , name="product_list"),

    path("product_detail/<slug:slug>/", ProductDetailView.as_view(), name="product_detail"),
    path("add_item/", AddItemView.as_view(), name="add_item"),
    path("product_in_cart/", ProductInCartView.as_view(), name="product_in_cart"),
    path("get_cart_start/", CartStartView.as_view(), name="get_cart_start"),
    path("get_cart/", CartDetailView.as_view(), name="get_cart"),
    path("update_quantity/", UpdateQuantityView.as_view(), name="update_quantity"),
    path("delete_cartitem/", DeleteCartItemView.as_view(), name="delete_cartitem"),

    path("get_username/", UsernameView.as_view(), name="get_username"),
    path("user_info/", UserInfoView.as_view(), name="user_info"),
]
