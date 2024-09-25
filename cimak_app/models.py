from django.db import models

class Car(models.Model):
    car_number = models.CharField(max_length=15, unique=True)  # تعيين unique=True لمنع القيم المكررة
    car_model = models.CharField(max_length=30)
    car_color = models.CharField(max_length=15)

    def __str__(self):
        return self.car_number

class Booking(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='bookings')  # إضافة related_name
    status = models.CharField(max_length=10, default='pending')
    arrival_date = models.DateField(null=True, blank=True)  # إضافة الحقل الجديد

    class Meta:
        permissions = [
            ("can_view_manager", "يمكنه عرض صفحة الإدارة"),
            ("can_edit_data_entry", "يمكنه إدخال البيانات"),
            ("can_view_accepted_bookings", "يمكنه عرض الحجوزات المقبولة"),  # صلاحية جديدة
        ]

    def __str__(self):
        return f"{self.car.car_number} - {self.status}"

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        # تحقق مما إذا كانت السيارة لا تحتوي على حجوزات أخرى
        if not self.car.bookings.exists():
            self.car.delete()  # اتاكيد السيارة إذا لم يكن هناك حجوزات متبقية
