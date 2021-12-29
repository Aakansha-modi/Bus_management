from datetime import datetime
from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import *
from .forms import CreateUserForm
from datetime import date
import calendar
import datetime


def registerPage(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			form.save()
		else:
			messages.info(request, 'User with this email already exists')
	context = {'form':form}
	return render(request, 'accounts/register.html', context)

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            login_obj = AdminUser.objects.filter(admin_id = user).first()
            if login_obj:
                return redirect('/admin_home')
            else:    
                return redirect('/home')
        else:
            messages.info(request, 'username OR password incorrect')
    return render(request, 'accounts/login.html')

def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
def driver(request):
    allD=Driver.objects.all()
    context={'allD': allD} 
    return render(request,'accounts/driver.html',context)


@login_required(login_url='login')
def add_driver(request):
    if request.method == 'POST':
            if request.POST.get('name') and request.POST.get('phone_number') and request.POST.get('licenese_number'):
                post=Driver()
                post.name= request.POST.get('name')
                post.phone_number= request.POST.get('phone_number')
                post.licenese_number= request.POST.get('licenese_number')
                post.save()
                
                return render(request, 'accounts/add_driver.html')  
            

    else:
        return render(request,'accounts/add_driver.html')

@login_required(login_url='login')
def home(request):
    user1 = request.user
    user_email=user1.username
    
    
    return render(request, 'accounts/user_home.html',{'user_email':user_email})
   

@login_required(login_url='login')
def admin_home(request):
    return render(request,'accounts/admin_home.html')

@login_required(login_url='login')
def delete_driver(request,id):
    obj=Driver.objects.get(driver_id=id)
    obj.delete()
    return redirect('driver')

@login_required(login_url='login')
def add_request(request):
    if request.method == 'POST':
            if request.POST.get('departure_time') and request.POST.get('startpoint') and request.POST.get('endpoint') and request.POST.get('number_seats'):
                post=Request()
                name=request.user.email
                user_obj = User.objects.filter(email = name).first()
                post.user_email= user_obj
                post.departure_time= request.POST.get('departure_time')
                post.startpoint= request.POST.get('startpoint')
                post.endpoint= request.POST.get('endpoint')
                post.number_seats= request.POST.get('number_seats')
               
                post.save()
                
                return render(request, 'accounts/add_request.html')  
            

    else:
       
        return render(request,'accounts/add_request.html')

@login_required(login_url='login')
def request(request):
    allD=Request.objects.all()
    context={'allD': allD} 
    return render(request,'accounts/request.html',context)


@login_required(login_url='login')
def add_bus(request):
    if request.method == 'POST':
        if request.POST.get('availability') and request.POST.get('capacity') and request.POST.get('driver_id'):
            post=Bus()
            post.availability= request.POST.get('availability')
            post.capacity= request.POST.get('capacity')
            name=request.POST.get('driver_id')
            driver_obj = Driver.objects.filter(driver_id = name).first()
            post.driver_id = driver_obj
            post.save()
            return render(request,'accounts/add_bus.html')
    else:
        return render(request,'accounts/add_bus.html')

@login_required(login_url='login')
def bus(request):
    allD=Bus.objects.all()
    context={'allD': allD} 
    return render(request,'accounts/bus.html',context)

def delete_bus(request,id):
    obj=Bus.objects.get(bus_id=id)
    obj.delete()
    return redirect('bus')

@login_required(login_url='login')
def add_schedule(request):
    if request.method == 'POST':
            if request.POST.get('time') and request.POST.get('start') and request.POST.get('destination')  and request.POST.get('available_seats')  and request.POST.get('day') and request.POST.get('running_status') and request.POST.get('bus_id'):
                post=Schedule()
                bus_id=request.POST.get('bus_id')
                
                bus_obj = Bus.objects.filter(bus_id = bus_id).first()
                post.bus_id= bus_obj
                post.time= request.POST.get('time')
                post.start= request.POST.get('start')
                post.destination= request.POST.get('destination')
                post.available_seats= request.POST.get('available_seats')
                post.day= request.POST.get('day')
                post.running_status= request.POST.get('running_status')
                post.save()
                return render(request, 'accounts/add_schedule.html')  
    else:
        return render(request,'accounts/add_schedule.html')


@login_required(login_url='login')
def view_schedule(request):
    allD=Schedule.objects.all()
    context={'allD': allD} 
    return render(request,'accounts/View_schedule.html',context)

@login_required(login_url='login')
def delete_schedule(request,id):
    obj=Schedule.objects.get(schedule_id=id)
    obj.delete()
    return redirect('add_schedule')


@login_required(login_url='login')
def add_wallet(request):
    if request.method == 'POST':
            if request.POST.get('wallet_id') and request.POST.get('balance'):
                post=Wallet()
                wallet_id=request.POST.get('wallet_id')
                bus_obj = User.objects.filter(email = wallet_id).first()
                post.wallet_id= bus_obj
                post.balance= request.POST.get('balance')
                post.save()
                return render(request, 'accounts/add_wallet.html')  
    else:
        return render(request,'accounts/add_wallet.html')


@login_required(login_url='login')
def book_bus(request):
    date=timezone.now().date()
    curr_date = date.today()
    curr_day = calendar.day_name[curr_date.weekday()]
    allD=Schedule.objects.filter(day='Friday')
    context={'allD': allD,'date':date,'curr_day':curr_day}
    return render(request,'accounts/Book_bus.html',context)

@login_required(login_url='login')
def booking(request,id):
    if request.method == 'POST':
            if request.POST.get('seat_no'):
                seats = request.POST.get('seat_no')
                amount = 25*(int(seats))
                user = request.user
                email = user.email
                i=1
                wallet_obj = Wallet.objects.filter(wallet_id = user).first()
                if int(wallet_obj.balance) < int(amount):
                    messages.info(request, 'Your Balance is low')
                    i=0
                seats_obj = Schedule.objects.filter(schedule_id = id).first()
                if int(seats)<0:
                    messages.info(request, 'Please enter correct seat number')
                    i=0
                if int(seats_obj.available_seats) < int(seats):
                    messages.info(request, 'Seats are not available')
                    i=0
                if i==0:
                    return redirect('/book_bus')    
                wallet_obj.balance = wallet_obj.balance - int(amount)
                wallet_obj.save()
                seats_obj.available_seats = seats_obj.available_seats- int(seats)
                seats_obj.save()
                post=Booking()
                date = datetime.datetime.now()
                post.date_time = date
                bus_obj = User.objects.filter(email = email ).first()
                post.user_email= bus_obj
                post.seat_no= seats
                
                schedule_id=id
                bus_ob = Schedule.objects.filter(schedule_id = schedule_id ).first()
                post.schedule_id = bus_ob
                post.save()
                return render(request, 'accounts/booking.html')
    else:
        user=request.user 
        seats_obj = Schedule.objects.filter(schedule_id = id).first()
        seats = seats_obj.available_seats
        wallet_obj = Wallet.objects.filter(wallet_id = user).first()
        if(wallet_obj is None):
            messages.info(request, 'You dont have wallet')
            return redirect('/book_bus')
        amount=wallet_obj.balance
        return render(request,'accounts/booking.html',{'seats' : seats,'amount':amount})


def schedule(request,data=None):
    if data==None:
        sch=Schedule.objects.filter(day='Monday')
        context={'sch': sch}
    elif data=='Monday':
        sch=Schedule.objects.filter(day='Monday')
        context={'sch': sch}
    elif data=='Tuesday':
        sch=Schedule.objects.filter(day='Tuesday')
        context={'sch': sch}
    elif data=='Wednesday':
        sch=Schedule.objects.filter(day='Wednesday')
        context={'sch': sch}
    elif data=='Thrusday':
        sch=Schedule.objects.filter(day='Thrusday')
        context={'sch': sch}
    elif data=='Friday':
        sch=Schedule.objects.filter(day='Friday')
        context={'sch': sch}
    elif data=='Saturday':
        sch=Schedule.objects.filter(day='Saturday')
        context={'sch': sch}
    elif data=='Sunday':
        sch=Schedule.objects.filter(day='Sunday')
        context={'sch': sch}
    return render(request, 'accounts/schedule.html',context)

@login_required(login_url='login')
def view_booking(request):
    user = request.user
    booking_obj = Booking.objects.filter(user_email = user).all()
    print(booking_obj)
    schedule_obj = Schedule.objects.all()
    return render(request,'accounts/Past_bookings.html',{'booking_obj' : booking_obj, 'schedule_obj' : schedule_obj})





	



