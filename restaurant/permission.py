from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
   def has_permission(self, request, view):
      if request.method in permissions.SAFE_METHODS:
         return True
      return request.user.is_authenticated and request.user.role == 'admin'

class IsAdminOnly(permissions.BasePermission):
   def has_permission(self, request, view):
      return request.user.is_authenticated and request.user.role == 'admin'

class IsManagerOrReadOnly(permissions.BasePermission):
   def has_permission(self, request, view):
      if request.method in permissions.SAFE_METHODS:
         return True
      return request.user.is_authenticated and request.user.role == 'manager'

class IsManagerOnly(permissions.BasePermission):
   def has_permission(self, request, view):
      return request.user.is_authenticated and request.user.role == 'manager'

class IsWaiterOrReadOnly(permissions.BasePermission):
   def has_permission(self, request, view):
      if request.method in permissions.SAFE_METHODS:
         return True
      return request.user.is_authenticated and request.user.role == 'waiter'

class IsWaiterOnly(permissions.BasePermission):
   def has_permission(self, request, view):
      return request.user.is_authenticated and request.user.role == 'waiter'

class IsChefOrReadOnly(permissions.BasePermission):
   def has_permission(self, request, view):
      if request.method in permissions.SAFE_METHODS:
         return True
      return request.user.is_authenticated and request.user.role == 'chef'

class IsChefOnly(permissions.BasePermission):
   def has_permission(self, request, view):
      return request.user.is_authenticated and request.user.role == 'chef'

class IsCashierOrReadOnly(permissions.BasePermission):
   def has_permission(self, request, view):
      if request.method in permissions.SAFE_METHODS:
         return True
      return request.user.is_authenticated and request.user.role == 'cashier'

class IsCashierOnly(permissions.BasePermission):
   def has_permission(self, request, view):
      return request.user.is_authenticated and request.user.role == 'cashier'

class IsRoleAllowed(permissions.BasePermission):
   def has_permission(self,request,view):
      return request.user.is_authenticated and request.user.role is not None