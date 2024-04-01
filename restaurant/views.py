from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import *
from .permission import *
# Create your views here.

class MenuGeneric(generics.ListAPIView,generics.CreateAPIView):
   queryset = Menu.objects.all()
   serializer_class = MenuSerializer
   permission_classes = [IsAdminOrReadOnly]
class MenuGeneric2(generics.RetrieveUpdateDestroyAPIView):
   queryset = Menu.objects.all()
   serializer_class = MenuSerializer
   lookup_field = 'id'
   permission_classes = [IsAdminOnly]
class TableGeneric(generics.ListCreateAPIView):
   queryset = Table.objects.all()
   serializer_class = TableSerializer
   permission_classes = [IsAdminOrReadOnly |IsManagerOnly] 

class TableGeneric2(generics.RetrieveUpdateAPIView):
   queryset = Table.objects.all()
   serializer_class = TableSerializer2
   lookup_field = 'id'
   permission_classes = [IsAdminOnly |IsManagerOnly | IsWaiterOnly]   
class OrderGeneric(generics.ListCreateAPIView):
   queryset = Order.objects.prefetch_related('items')
   serializer_class = OrderSerializer
   permission_classes = [IsWaiterOrReadOnly]

class OrderGeneric2(generics.RetrieveUpdateDestroyAPIView):
   queryset = Order.objects.prefetch_related('items')
   serializer_class = OrderSerializer
   lookup_field = 'id'  
   permission_classes = [IsWaiterOrReadOnly]

class OrderItemGeneric(generics.ListCreateAPIView):
   # queryset = OrderItem.objects.select_related('item')
   serializer_class = OrderItemSerializer
   permission_classes = [IsWaiterOrReadOnly]
   def get_queryset(self):
      order_id = self.kwargs['order_id']
      return OrderItem.objects.filter(order_id=order_id)
   def perform_create(self, serializer):
      order_id = self.kwargs.get('order_id')
      serializer.save(order_id=order_id)
class OrderItemGeneric2(generics.RetrieveUpdateDestroyAPIView):
   serializer_class = OrderItemSerializer
   permission_classes = [IsWaiterOrReadOnly]
   def get_queryset(self):
      order_id = self.kwargs['order_id']
      return OrderItem.objects.filter(order_id=order_id)  
   lookup_field = 'id'   

class KitchenGeneric(generics.ListCreateAPIView):
   queryset = Kitchen.objects.all()
   serializer_class = KitchenSerializer 
   permission_classes = [IsWaiterOrReadOnly | IsChefOnly]

class KitchenGeneric2(generics.RetrieveUpdateDestroyAPIView):
   queryset = Kitchen.objects.all()
   serializer_class = KitchenSerializer 
   lookup_field = 'id' 
   permission_classes = [IsChefOnly]

class BillGeneric(generics.ListCreateAPIView):
   queryset = Bill.objects.all()
   serializer_class = BillSerializer 
   permission_classes = [IsRoleAllowed]

class BillGeneric2(generics.RetrieveUpdateDestroyAPIView):
   queryset = Bill.objects.all()
   serializer_class = BillSerializer
   lookup_field = 'id'  
   permission_classes = [IsRoleAllowed]

class IngredientGeneric(generics.ListCreateAPIView):
   queryset = Ingredient.objects.all()
   serializer_class = IngredientSerializer
   permission_classes = [IsRoleAllowed]

class InventoryItemGeneric(generics.ListCreateAPIView):
   queryset = InventoryItem.objects.all()
   serializer_class = InventoryItemSerializer
   permission_classes = [IsRoleAllowed]

class InventoryItemGeneric2(generics.RetrieveUpdateDestroyAPIView):
   queryset = InventoryItem.objects.all()
   serializer_class = InventoryItemSerializer
   lookup_field = 'id'
   permission_classes = [IsRoleAllowed]

# class StaffGeneric(generics.ListCreateAPIView):
#    queryset = Staff.objects.all()
#    serializer_class = StaffSerializer
#    permission_classes = [IsAdminOrReadOnly | IsManagerOnly]

# class Staff(generics.RetrieveUpdateDestroyAPIView):
#    queryset = Staff.objects.all()
#    serializer_class = StaffSerializer
#    permission_classes = [IsAdminOnly | IsManagerOnly]
#    lookup_field= 'id'