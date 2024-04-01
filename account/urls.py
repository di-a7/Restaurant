from django.urls import path, include
from .views import *

urlpatterns = [
   path('register/', RegistrationAPIView.as_view(), name='user-registration'),
   path('login/', LoginAPIView.as_view(), name='user-login'),
   path('logout/', LogoutAPIView.as_view(), name='user-logout'),
   
   path('staff/', StaffGeneric.as_view()),
   path('staff/<id>', Staff.as_view()),
   
   path('shift/', ShiftGeneric.as_view()),
   path('shift/<id>', Shift.as_view()),
   
   path('timeoff/', TimeOffRequestGeneric.as_view()),
   path('timeoff/<id>', TimeOffRequest.as_view()),
   
]
