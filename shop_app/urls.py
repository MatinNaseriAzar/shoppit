from django.urls import path
from . import views
from .views import products


urlpatterns = [
    path("products/", products.as_view() ,name="products"),
    path("product_detail/<slug:slug>/",views.product_detail,name='product_detail'),
    path("add_item/",views.add_item,name="add_item"),
    path("product_in_cart/",views.product_in_cart,name="product_in_cart"),
    path("get_cart_start/",views.get_cart_start,name="get_cart_start"),
    path("get_cart/",views.get_cart,name="get_cart"),
    path("update_quantity/",views.update_quantity,name="update_quantity"),
    path("delete_cartitem/",views.delete_cartitem,name="delete_cartitem"),
    path("get_username/",views.get_username,name="get_username"),
    path("user_info/",views.user_info,name="user_info"),
    # path("initiate_payment/",views.initiate_payment,name="initiate_payment")
]
