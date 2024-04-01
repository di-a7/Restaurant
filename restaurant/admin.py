from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
   list_display=['name','category','description','display_price'] 
   search_fields=('name','category')
   list_filter=('category','price',)
   list_per_page=15
   
   def display_price(self,obj):
      return f"Rs. {obj.price}"
   display_price.short_description = 'Price'

class TableInline(admin.TabularInline):
   model = Table

class OrderItemInline(admin.TabularInline):
   model = OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
   list_display= ['id','user','order_type','status','table','display_order_items','total_amount']
   list_editable= ('status',)
   search_fields=('user','order_type','status',)
   list_filter=('order_type','status','table','user')
   list_per_page=15
   
   inlines = (OrderItemInline,)
   
   def display_order_items(self, obj):
      order_items = ", ".join([f"{item.quantity}x {item.menu.name} ({item.special_requests}.)" for item in obj.items.all()])
      return order_items if order_items else "-"
   display_order_items.short_description = "Order Items"
   
   def total_amount(self, obj):
      total = sum(item.menu.price * item.quantity for item in obj.items.all())
      return total

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
   list_display= ['table_number','capacity','status']
   list_editable= ('status',)
   search_fields=('capacity','status')
   list_filter=('table_number','status','capacity')
@admin.register(Kitchen)
class KitchenAdmin(admin.ModelAdmin):
   list_display=['order','order_type','display_special_requests','preparation_status']
   list_editable= ('preparation_status',)
   search_fields=('preparation_status',)
   list_filter=('preparation_status','order',)
   
   def display_special_requests(self, obj):
      order_items = " ".join([f"{item.quantity}x {item.menu.name} ({item.special_requests}.)" for item in obj.order.items.all()])
      return order_items if order_items else "-"
   display_special_requests.short_description = "Order Item"
   
   def order_type(self,obj):
      return obj.order.order_type
   order_type.short_description = 'Order Type'
   
   def get_form(self, request, obj=None, **kwargs):
      form = super().get_form(request, obj, **kwargs)
      if obj is None:  
         existing_orders = Kitchen.objects.all().values_list('order', flat=True)
         form.base_fields['order'].queryset = Order.objects.exclude(pk__in=existing_orders)
      return form
@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
   list_display=['order','display_order_items','total_amount','generated_by','generated_at']
   search_fields=('generated_by__username',)
   list_filter=('order','generated_by','order__table__table_number',)
   list_per_page=15
   
   def display_order_items(self, obj):
      order_items = ", ".join([f"{item.quantity}x {item.menu.name} ({item.special_requests}.)" for item in obj.order.items.all()])
      return order_items if order_items else "-"
   display_order_items.short_description = "Order Items"
   
   def total_amount(self, obj):
      total = sum(item.menu.price * item.quantity for item in obj.order.items.all())
      return total
   total_amount.short_description = "Total Amount"
   
   def get_form(self, request, obj=None, **kwargs):
      form = super().get_form(request, obj, **kwargs)
      if obj is None:  
         existing_orders = Bill.objects.all().values_list('order', flat=True)
         form.base_fields['order'].queryset = Order.objects.exclude(pk__in=existing_orders)
      return form

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
   list_display=['name']
   search_fields=('name',)
   list_per_page=15

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
   list_display=['ingredient','quantity','unit_of_measurement','used_quantity','expiration_date']
   list_editable= ('used_quantity',)
   search_fields= ('ingredient__name','quantity','expiration_date')
   autocomplete_fields = ('ingredient',)
   list_filter=('ingredient','used_quantity','expiration_date')
   list_per_page=15

