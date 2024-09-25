from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Car, Booking

def is_data_entry_user(user):
    return user.has_perm('cimak_app.can_edit_data_entry')

def is_manager_user(user):
    return user.has_perm('cimak_app.can_view_manager')

def is_accepted_bookings_viewer(user):
    return user.has_perm('cimak_app.can_view_accepted_bookings')

def home_view(request):
    bookings = []
    car = None
    car_not_found = False  # متغير للتحقق من عدم وجود السيارة
    if request.method == 'POST':
        car_number = request.POST.get('car_number')
        car = Car.objects.filter(car_number=car_number).first()
        if car:
            bookings = Booking.objects.filter(car=car).order_by('-arrival_date')
        else:
            car_not_found = True  # تعيين المتغير إلى True عند عدم وجود السيارة
    return render(request, 'home.html', {'car': car, 'bookings': bookings, 'car_not_found': car_not_found})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, 'لقد تم التسجيل بنجاح!')
            return redirect('data_entry')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'لقد تم الدخول بنجاح!')

                # تحقق من صلاحيات المستخدم
                if user.has_perm('cimak_app.can_edit_data_entry'):
                    return redirect('data_entry')  # توجيه مدخل البيانات
                elif user.has_perm('cimak_app.can_view_manager'):
                    return redirect('manager')  # توجيه المدير
                elif user.has_perm('cimak_app.can_view_accepted_bookings'):
                    return redirect('accepted_bookings')  # توجيه عارض الحجوزات المقبولة
                elif user.is_superuser:  # توجيه المستخدمين الخارقين
                    return redirect('admin:index')  # توجيه إلى واجهة الإدارة
                else:
                    return redirect('home')  # توجيه المستخدم العادي إلى الصفحة الرئيسية
            else:
                messages.error(request, 'خطأ في اسم المستخدم أو كلمة المرور!')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
@user_passes_test(is_data_entry_user)
def data_entry_view(request):
    if request.method == 'POST':
        car_number = request.POST.get('car_number')
        car_model = request.POST.get('car_model')
        car_color = request.POST.get('car_color')

        car, created = Car.objects.get_or_create(car_number=car_number, defaults={'car_model': car_model, 'car_color': car_color})

        existing_booking = Booking.objects.filter(car=car, status__in=['pending', 'approved']).exists()
        if not existing_booking:
            booking = Booking(car=car, status='pending')
            booking.save()
            messages.success(request, 'لقد تم إدخال البيانات وحجز السيارة بنجاح!')
        else:
            messages.warning(request, 'توجد بالفعل حجز للسيارة!')

        return redirect('data_entry')

    return render(request, 'data_entry.html')

@login_required
@user_passes_test(is_manager_user)
def manager_view(request):
    bookings = Booking.objects.filter(status='pending').select_related('car')
    return render(request, 'manager.html', {'bookings': bookings})

@login_required
@user_passes_test(is_manager_user)
def approve_booking(request, pk):
    try:
        booking = Booking.objects.get(pk=pk)
        if request.method == 'POST':
            arrival_date = request.POST.get('arrival_date')
            booking.status = 'approved'
            booking.arrival_date = arrival_date
            booking.save()
            messages.success(request, 'تمت الموافقة على الحجز بنجاح!')
        else:
            messages.error(request, 'طريقة الطلب غير صحيحة.')
    except Booking.DoesNotExist:
        messages.error(request, 'لم يتم العثور على الحجز.')
    return redirect('manager')

@login_required
@user_passes_test(is_manager_user)
def reject_booking(request, pk):
    try:
        booking = Booking.objects.get(pk=pk)
        booking.delete()
        messages.success(request, 'تم رفض الحجز وإزالته بنجاح!')
    except Booking.DoesNotExist:
        messages.error(request, 'لم يتم العثور على الحجز.')
    return redirect('manager')

@login_required
@user_passes_test(is_accepted_bookings_viewer)
def accepted_bookings_view(request):
    accepted_bookings = Booking.objects.filter(status='approved').select_related('car')
    return render(request, 'accepted_bookings.html', {'bookings': accepted_bookings})

@login_required
@user_passes_test(is_manager_user)
def delete_booking_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        booking.delete()
        messages.success(request, 'تم تاكيد الحجز بنجاح!')
        return redirect('accepted_bookings')
    return render(request, 'delete_booking.html', {'booking': booking})

@login_required
@user_passes_test(is_manager_user)
def car_view(request):
    cars = Car.objects.all()
    return render(request, 'car.html', {'cars': cars})