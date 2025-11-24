from django.shortcuts import render
from rest_framework.decorators import api_view , permission_classes
from .models import Product , Cart , CartItem , Transaction
from .serializers import ProductSerializer , DetailProductSerializer , CartItemSerializer , CartSimpleSerializer , CartSerializer , UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from decimal import Decimal
import uuid
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet


BASE_URL = ""

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['category']

@api_view(["GET"])
def product_detail(request,slug):
    product = Product.objects.get(slug=slug)
    serializer = DetailProductSerializer(product)
    return Response(serializer.data)

@api_view(["POST"])
def add_item(request):
    try :
        cart_code = request.data.get("cart_code")
        product_id = request.data.get("product_id")

        #پیدا کردن Cart با cart_code 
        cart , created = Cart.objects.get_or_create(cart_code = cart_code)
        product=  Product.objects.get(id=product_id)

        cartitem , created = CartItem.objects.get_or_create(cart=cart , product=product)
        cartitem.quantity = 1
        cartitem.save()

        serializer = CartItemSerializer(cartitem)
        return Response({"detail":serializer.data, "message": "CartItem created succcessfully"} , status=201)
    
    except Exception as e :
        return Response({"error": str(e)}, status=400)
    

@api_view(["GET"])
def product_in_cart(request):
    cart_code = request.query_params.get("cart_code")
    product_id = request.query_params.get("product_id")
    
    cart = Cart.objects.get(cart_code=cart_code)
    product = Product.objects.get(id=product_id)

    product_exists_in_cart = CartItem.objects.filter(cart=cart,product=product).exists()

    return Response({'product_in_cart':product_exists_in_cart})

@api_view(["GET"])
def get_cart_start(request):
    cart_code = request.query_params.get("cart_code")
    cart = Cart.objects.get(cart_code=cart_code,paid=False)
    serializer = CartSimpleSerializer(cart)
    return Response(serializer.data)


@api_view(["GET"])
def get_cart(request):
    cart_code = request.query_params.get("cart_code")
    cart = Cart.objects.get(cart_code=cart_code,paid=False)
    serializer = CartSerializer(cart)
    return Response(serializer.data)


@api_view(["PATCH"])
def update_quantity(request):
    try:
        cartitem_id = request.data.get("item_id")
        quantity = request.data.get("quantity")
        quantity = int(quantity)
        cartitem = CartItem.objects.get(id=cartitem_id)
        cartitem.quantity = quantity
        cartitem.save()
        serializer = CartItemSerializer(cartitem)
        return Response({"data":serializer.data ,"message": "Cartitem  updated successfully"})
    except Exception as e :
        return Response({"error":str(e),},status=400)
    

@api_view(["DELETE"])
def delete_cartitem(request):
    cartitem_id = request.data.get("item_id")
    cartitem = CartItem.objects.get(id=cartitem_id)
    cartitem.delete()
    return Response({"message":"item deleted successfully"},status=status.HTTP_204_NO_CONTENT)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_username(request):
    user = request.user
    return Response({"username": user.username})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_info(request):
    user=request.user
    serializer = UserSerializer(user)
    return  Response(serializer.data)

# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def initiate_payment(request):
#     if request.user:
#         try:
#             tx_ref = str(uuid.uuid4())
#             cart_code = request.data.get("cart_code")
#             cart = Cart.objects.get(cart_code=cart_code)
#             user = request.user

#             amount = sum([item.quantity * item.product.price for item in cart.items.all()])
#             tax = Decimal("4.00")
#             total_amount = amount + tax
#             currency = "USD"
#             redirect_url = f"{BASE_URL}/payment-status"

#             transaction = Transaction.objects.create(
#                 ref=tx_ref,
#                 cart=cart,
#                 amount=total_amount,
#                 currency=currency,
#                 user=user,
#                 status='pending'
#             )
