from django.shortcuts import render
from rest_framework.decorators import api_view , permission_classes
from .models import Product , Cart , CartItem , Transaction
from .serializers import ProductSerializer , DetailProductSerializer , CartItemSerializer , CartSimpleSerializer , CartSerializer , UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework import mixins 
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import RetrieveAPIView , CreateAPIView , UpdateAPIView , DestroyAPIView , ListAPIView


BASE_URL = ""

class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['category']


class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = DetailProductSerializer
    lookup_field = 'slug'
    

# @api_view(["POST"])
# def add_item(request):
#     try :
#         cart_code = request.data.get("cart_code")
#         product_id = request.data.get("product_id")

#         #پیدا کردن Cart با cart_code 
#         cart , created = Cart.objects.get_or_create(cart_code = cart_code)
#         product=  Product.objects.get(id=product_id)

#         cartitem , created = CartItem.objects.get_or_create(cart=cart , product=product)
#         cartitem.quantity = 1
#         cartitem.save()

#         serializer = CartItemSerializer(cartitem)
#         return Response({"detail":serializer.data, "message": "CartItem created succcessfully"} , status=201)
    
#     except Exception as e :
#         return Response({"error": str(e)}, status=400)
    
class AddItemView(CreateAPIView):
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()

    def create(self,request,*args,**kwargs):
        try:
            cart_code = request.data.get("cart_code")
            product_id = request.data.get("product_id")

            cart , created = Cart.objects.get_or_create(cart_code = cart_code)
            product = Product.objects.get(id=product_id)

            cartitem , created = CartItem.objects.get_or_create(
                cart=cart , product = product
            )

            cartitem.quantity = 1
            cartitem.save()

            serializer = CartItemSerializer(cartitem)
            return Response(
                {"detail":serializer.data, "message" : "CartItem created successfully"},
                status=201
            )
        except Exception as  e :
            return Response({"error":str(e)},status=400)


# @api_view(["GET"])
# def product_in_cart(request):
#     cart_code = request.query_params.get("cart_code")
#     product_id = request.query_params.get("product_id")
    
#     cart = Cart.objects.get(cart_code=cart_code)
#     product = Product.objects.get(id=product_id)

#     product_exists_in_cart = CartItem.objects.filter(cart=cart,product=product).exists()

#     return Response({'product_in_cart':product_exists_in_cart})

class ProductInCartView(GenericAPIView):
    def get(self,request):
        cart_code= request.query_params.get("cart_code")
        product_id = request.query_params.get("product_id")

        cart = Cart.objects.get(cart_code = cart_code)
        product = Product.objects.get(id=product_id)

        exists = CartItem.objects.filter(cart=cart, product=product).exists()

        return Response({"product_in_cart":exists})

# @api_view(["GET"])
# def get_cart_start(request):
#     cart_code = request.query_params.get("cart_code")
#     cart = Cart.objects.get(cart_code=cart_code,paid=False)
#     serializer = CartSimpleSerializer(cart)
#     return Response(serializer.data)

class CartStartView(RetrieveAPIView):
    serializer_class = CartSimpleSerializer

    def get_object(self):
        cart_code = self.request.query_params.get("cart_code")
        return Cart.objects.get(cart_code=cart_code,paid=False)


# @api_view(["GET"])
# def get_cart(request):
#     cart_code = request.query_params.get("cart_code")
#     cart = Cart.objects.get(cart_code=cart_code,paid=False)
#     serializer = CartSerializer(cart)
#     return Response(serializer.data)

class CartDetailView(RetrieveAPIView):
    serializer_class = CartSerializer

    def get_object(self):
        cart_code = self.request.query_params.get("cart_code")
        return Cart.objects.get(cart_code=cart_code,paid = False)


# @api_view(["PATCH"])
# def update_quantity(request):
#     try:
#         cartitem_id = request.data.get("item_id")
#         quantity = request.data.get("quantity")
#         quantity = int(quantity)
#         cartitem = CartItem.objects.get(id=cartitem_id)
#         cartitem.quantity = quantity
#         cartitem.save()
#         serializer = CartItemSerializer(cartitem)
#         return Response({"data":serializer.data ,"message": "Cartitem  updated successfully"})
#     except Exception as e :
#         return Response({"error":str(e),},status=400)
    

class UpdateQuantityView(UpdateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def update(self,request,*args,**kwargs):
        try :
            item_id = request.data.get("item_id")
            quantity = int(request.data.get("quantity"))

            CartItem = CartItem.objects.get(id=item_id)
            CartItem.quantity = quantity
            CartItem.save()

            serializer = CartItemSerializer(CartItem)
            return Response({"data":serializer.data, "message" : "updated successfully"})
        except Exception as e :
            return Response({"error":str(e)},status=400)


# @api_view(["DELETE"])
# def delete_cartitem(request):
#     cartitem_id = request.data.get("item_id")
#     cartitem = CartItem.objects.get(id=cartitem_id)
#     cartitem.delete()
#     return Response({"message":"item deleted successfully"},status=status.HTTP_204_NO_CONTENT)


class DeleteCartItemView(DestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def delete(self,request,*args,**kwargs):
        item_id = request.data.get("item_id")
        cartitem = CartItem.objects.get(id=item_id)
        cartitem.delete()
        return Response({"message":"item deleted successfully"}, status=204)
    

# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def get_username(request):
#     user = request.user
#     return Response({"username": user.username})

class UsernameView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    def retrieve(self, request, *args, **kwargs):
        return Response({"username":request.user.username})


# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def user_info(request):
#     user=request.user
#     serializer = UserSerializer(user)
#     return  Response(serializer.data)

class UserInfoView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


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
