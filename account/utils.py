from django.db.models import Sum
from datetime import datetime
from .models import ShiftLog
def calculate_hours_worked(staff, start_date, end_date):
   """Calculate total hours worked by a staff member within a date range."""
   shift_logs = ShiftLog.objects.filter(staff=staff, date__range=[start_date, end_date])
   total_hours = shift_logs.aggregate(total=Sum('end_time') - Sum('start_time'))['total']
   return total_hours