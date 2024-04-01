from rest_framework import serializers
from .models import *

class MenuSerializer(serializers.ModelSerializer):
   class Meta:
      model = Menu
      # fields = ['name','category','description','price']
      # exclude = ['id',]
      fields = '__all__'

class TableSerializer(serializers.ModelSerializer):
   class Meta:
      model = Table
      # fields = '__all__'
      exclude = ['id',]

class TableSerializer2(serializers.ModelSerializer):
   class Meta:
      model = Table
      # fields = '__all__'
      exclude = ['id',]
      read_only_fields = ['id', 'table_number', 'capacity']

class OrderItemSerializer(serializers.ModelSerializer):
   menu_id = serializers.PrimaryKeyRelatedField(
      queryset = Menu.objects.all(),
      source = "menu"
   )
   menu= serializers.StringRelatedField()
   class Meta:
      model = OrderItem
      exclude = ['order',]

class OrderSerializer(serializers.ModelSerializer):
   order_items = OrderItemSerializer(many=True, source='items',read_only = True)
   user = serializers.StringRelatedField()
   class Meta: 
      model = Order
      fields = ['id', 'user', 'order_type', 'table', 'status','order_items',] 

class KitchenSerializer(serializers.ModelSerializer):
   order_type = serializers.CharField(source='order.order_type',read_only=True)
   special_request = serializers.SerializerMethodField()
   order = serializers.SerializerMethodField(read_only=True)
   order_id = serializers.PrimaryKeyRelatedField(
      queryset = Order.objects.all(),
      source = "order"
   )
   class Meta:
      model = Kitchen
      fields = ['id','order_id','order', 'order_type', 'special_request', 'preparation_status']

   def get_order(self, obj):
      order = obj.order
      if order:
         order_items = order.items.all()
         formatted_order = " ".join([f"{item.quantity}x {item.menu.name} ({item.special_requests})" for item in order_items])
         return formatted_order
      return None

   def get_special_request(self, obj):
      order = obj.order
      if order:
         special_requests = [item.special_requests for item in order.items.all()]
         return special_requests
      return None

   def get_fields(self, *args, **kwargs):
      fields = super().get_fields(*args, **kwargs)
      request = self.context.get('request', None)
      if request and request.method == 'POST':
         existing_order_ids = Kitchen.objects.values_list('order_id', flat=True)
         fields['order_id'].queryset = Order.objects.exclude(id__in=existing_order_ids)
      return fields

   def create(self, validated_data):
      order_id = validated_data.pop('order_id')
      kitchen = Kitchen.objects.create(**validated_data)
      kitchen.order = order_id
      return kitchen

class BillSerializer(serializers.ModelSerializer):
   order_type = serializers.CharField(source='order.order_type',read_only=True)
   # table = serializers.CharField(source= 'order.table',read_only = True)
   order_id = serializers.PrimaryKeyRelatedField(
      queryset = Order.objects.all(),
      source = "order"
   )
   order = serializers.StringRelatedField()
   user_id = serializers.PrimaryKeyRelatedField(
      queryset = User.objects.all(),
      source = "generated_by"
   )
   generated_by = serializers.StringRelatedField()
   total_amount = serializers.SerializerMethodField()
   # generated_at = serializers.DateTimeField(format="%Y-%m-%d %I:%M %p")
   class Meta:
      model = Bill
      fields = '__all__'

   def get_total_amount(self,cost:Bill):
      total_amount = sum(item.menu.price * item.quantity for item in cost.order.items.all())
      return total_amount

   def get_fields(self, *args, **kwargs):
      fields = super().get_fields(*args, **kwargs)
      request = self.context.get('request', None)
      if request and request.method == 'POST':
         existing_order_ids = Bill.objects.values_list('order_id', flat=True)
         fields['order_id'].queryset = Order.objects.exclude(id__in=existing_order_ids)
      return fields

   def create(self, validated_data):
      order_id = validated_data.pop('order_id',None)
      bill = Bill.objects.create(**validated_data)
      bill.order = order_id
      return bill

class IngredientSerializer(serializers.ModelSerializer):
   class Meta:
      model = Ingredient
      fields = '__all__'

class InventoryItemSerializer(serializers.ModelSerializer):
   ingredient_id = serializers.PrimaryKeyRelatedField(
      queryset = Ingredient.objects.all(),
      source = "ingredient"
   )
   ingredient = serializers.StringRelatedField()
   class Meta:
      model = InventoryItem
      fields = '__all__'
   def validate(self, data):
      if 'used_quantity' in data and data['used_quantity'] is not None and data['used_quantity'] > data['quantity']:
         raise serializers.ValidationError("Used quantity cannot exceed total quantity.")
      return data

class StaffSerializer(serializers.ModelSerializer):
   user_id = serializers.PrimaryKeyRelatedField(
      queryset = User.objects.exclude(role__isnull=True).exclude(staff__isnull=False),
      required=False, 
      source = "user"
   )
   user= serializers.StringRelatedField()
   user_role = serializers.SerializerMethodField()
   class Meta:
      model = Staff
      fields = '__all__'
   def get_user_role(self, obj):
      return obj.user.role if obj.user else None