from django.contrib import admin
from .models import Car, Booking

class CarAdmin(admin.ModelAdmin):
    list_display = ('car_number', 'car_model', 'car_color')  # عرض الحقول في واجهة الإدارة
    search_fields = ('car_number', 'car_model', 'car_color')  # إضافة خاصية البحث

class BookingAdmin(admin.ModelAdmin):
    list_display = ('car', 'status')  # عرض الحقول في واجهة الإدارة
    list_filter = ('status',)  # إضافة خاصية تصفية للحالة

admin.site.register(Car, CarAdmin)
admin.site.register(Booking, BookingAdmin)
