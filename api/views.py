from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Address
from .serializers import AddressSerializer, CheckoutSerializer

class AddressListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        addresses = Address.objects.filter(user=request.user)
        serializer = AddressSerializer(addresses, many=True)
        return Response({ 'addresses': serializer.data, 'default_address': next((a for a in serializer.data if a['is_default']), None) })
    
    def post(self, request):
        serializer = AddressSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddressDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk, user):
        return get_object_or_404(Address, pk=pk, user=user)
    
    def get(self, request, pk):
        address = self.get_object(pk, request.user)
        return Response(AddressSerializer(address).data)

    def put(self, request, pk):
        address = self.get_object(pk, request.user)
        serializer = AddressSerializer(address, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        address = self.get_object(pk, request.user)
        address.delete()
        return Response(
            {'message': 'Address deleted successfully'}, 
            status=status.HTTP_204_NO_CONTENT
        )
    
#Function-based view for setting default address
@api_view(['PATCH'])  
@permission_classes([IsAuthenticated])
def set_default_address(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    
    if address.is_default:
        return Response(
            {'message': 'This address is already the default.', 'address_id': address.id},
            status=status.HTTP_200_OK
        )
    
    address.is_default = True
    address.save()
    
    return Response(
        {
            'message': 'Default address updated successfully',
            'address_id': address.id,
            'address_summary': str(address)  
        },
        status=status.HTTP_200_OK
    )

#Function-based view for processing checkout
#Temporarily disabled until Cart and Order models are implemented, it is giving errors
'''@api_view(['POST'])
@permission_classes([IsAuthenticated])
def process_checkout(request):
    serializer = CheckoutSerializer(data=request.data, context={'request': request})

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Get cart; provided by Adilet
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        return Response(
            {'error': 'Cart not found.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    cart_items = cart.items.select_related('menu_item').all()
    if not cart_items.exists():
        return Response(
            {'error': 'Your cart is empty. Add items before checking out.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    data= serializer.validated_data
    address = get_object_or_404(Address, id=data['address_id'], user=request.user)
    total_price = sum(item.menu_item.price * item.quantity for item in cart_items)   
    
    #Akzhan's block, update then pls
    order = Order.objects.create(
        user=request.user,
        delivery_street=address.street,
        delivery_building=address.building,
        delivery_apartment=address.apartment or '',
        special_instructions=serializer.validated_data.get('special_instructions', ''),
        payment_method=serializer.validated_data['payment_method'],
        total_amount=total_price,
        status='pending'
    )
        
    for cart_item in cart_items:
        order.items.create(
            menu_item=cart_item.menu_item,
            quantity=cart_item.quantity,
            price_at_time=cart_item.menu_item.price
        )
    cart_items.delete()

    return Response({'message':'Order placed successfully',
                         'order_id': order.id,
                         'status': order.status,
                         'estimated_delivery': '30-45 minutes',
                         }, status=status.HTTP_201_CREATED)  '''