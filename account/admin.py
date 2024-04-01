from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

@admin.register(User)
class UserAdmin(UserAdmin):
   fieldsets = (
      (None, {"fields": ("username", "password")}),
      (("Personal info"), {"fields": ("first_name", "last_name", "email", "role")}),
      (
         ("Permissions"),
         {
            "fields": (
               "is_active",
               "is_staff",
               "is_superuser",
               "groups",
               "user_permissions",
            ),
         },
      ),
      (("Important dates"), {"fields": ("last_login", "date_joined")}),
   )
   list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'role')
   search_fields = ('username', 'email', 'first_name', 'last_name')
   ordering = ('username',)
   
   def save_model(self, request, obj, form, change):
      if obj.role is not None:
         obj.is_staff = True
      super().save_model(request, obj, form, change)
   list_filter=('role',)
   search_fields=('role','username')

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
   list_display = ('user','user_role','display_shift','contact')
   list_filter=('user__role','shifts__shift')
   search_fields=('role','username')
   # list_editable= ('display_shift',)
   def user_role(self, obj):
      return obj.user.role if obj.user else None
   user_role.short_description = 'Role'

   def display_shift(self, obj):
      return obj.shifts.first().get_shift_display() if obj.shifts.exists() else "No Shift"
   display_shift.short_description = 'Shift'

   def get_form(self, request, obj=None, **kwargs):
      form = super().get_form(request, obj, **kwargs)
      if obj is None: 
         existing_user_ids = Staff.objects.values_list('user_id', flat=True)
         form.base_fields['user'].queryset = User.objects.exclude(role__isnull=True).exclude(id__in=existing_user_ids)
      return form

@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
   list_display= ('staff','shift','date','start_time','end_time')
   list_editable=('shift','date')
   list_filter=('shift',)
   search_fields=('shift','username','date')

@admin.register(TimeOffRequest)
class TimeOffRequestAdmin(admin.ModelAdmin):
   list_display=('staff','status','date_from','date_to','comments')
   list_editable=('status',)
   list_filter=('status','date_from','comments')
   search_fields=('status','username','date')
