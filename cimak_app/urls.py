from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('data_entry/', views.data_entry_view, name='data_entry'),
    path('manager/', views.manager_view, name='manager'),
    path('accepted_bookings/', views.accepted_bookings_view, name='accepted_bookings'),  # إضافة مسار الحجوزات المقبولة
    path('approve/<int:pk>/', views.approve_booking, name='approve_booking'),
    path('reject/<int:pk>/', views.reject_booking, name='reject_booking'),
    path('booking/delete/<int:booking_id>/', views.delete_booking_view, name='delete_booking_view'),  # استيراد الدالة بشكل صحيح
]
