from django.contrib import admin
from .views import *
from django.urls import path

urlpatterns = [
   path('menu/', MenuGeneric.as_view()),
   path('menu/<id>/', MenuGeneric2.as_view()),

   path('table/', TableGeneric.as_view()),
   path('table/<id>', TableGeneric2.as_view()),
   

   path('order/', OrderGeneric.as_view()),
   path('order/<id>/', OrderGeneric2.as_view()),
   path('order/<int:order_id>/add/', OrderItemGeneric.as_view()),
   path('order/<int:order_id>/<id>/', OrderItemGeneric2.as_view()),

   path('kitchen/', KitchenGeneric.as_view()),
   path('kitchen/<id>', KitchenGeneric2.as_view()),

   path('bill/', BillGeneric.as_view()),
   path('bill/<id>/', BillGeneric2.as_view()),

   path('ingredient/', IngredientGeneric.as_view()),

   path('inventory/', InventoryItemGeneric.as_view()),
   path('inventory/<id>', InventoryItemGeneric2.as_view()),

]