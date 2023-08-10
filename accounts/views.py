from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Profile
import random
from twilio.rest import Client
from django.conf import settings
from django.contrib.auth import authenticate, login

# Create your views here.

account_sid = settings.TWILIO_ACCOUNT_SID
auth_token = settings.TWILIO_AUTH_TOKEN
twilio_phone_number = settings.TWILIO_PHONE_NUMBER

def send_otp(mobile, otp):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body='Your OTP is: ' + otp,
        from_=twilio_phone_number,
        to=mobile
    )

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        
        check_user = User.objects.filter(email=email).first()
        check_profile = Profile.objects.filter(mobile=mobile).first()
        
        if check_user or check_profile:
            context = {'message': 'User already exists', 'class': 'danger'}
            return render(request, 'register.html', context)
            
        user = User(email=email, first_name=name)
        user.save()
        otp = str(random.randint(1000, 9999))
        profile = Profile(user=user, mobile=mobile, otp=otp) 
        profile.save()
        send_otp(mobile, otp)
        request.session['mobile'] = mobile
        return redirect('otp')
    return render(request, 'register.html')

def otp(request):
    mobile = request.session.get('mobile')
    context = {'mobile': mobile}

    if not mobile:
        return redirect('register')

    if request.method == 'POST':
        otp = request.POST.get('otp')
        profile = Profile.objects.filter(mobile=mobile).first()

        if otp == profile.otp:
            return redirect('cart')
        else:
            context = {'message': 'Wrong OTP', 'class': 'danger', 'mobile': mobile}
            return render(request, 'otp.html', context)

    return render(request, 'otp.html', context)

def login_attempt(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile')

        user = Profile.objects.filter(mobile=mobile).first()

        if user is None:
            context = {'message': 'User not found', 'class': 'danger'}
            return render(request, 'login.html', context)

        otp = str(random.randint(1000, 9999))
        user.otp = otp
        user.save()
        send_otp(mobile, otp)
        request.session['mobile'] = mobile
        return redirect('login_otp')
    return render(request, 'login.html')

def login_otp(request):
    mobile = request.session.get('mobile')
    context = {'mobile': mobile}

    if not mobile:
        return redirect('login_attempt')

    if request.method == 'POST':
        otp = request.POST.get('otp')
        profile = Profile.objects.filter(mobile=mobile).first()

        if otp == profile.otp:
            user = User.objects.get(id=profile.user.id)
            login(request, user)
            return redirect('cart')
        else:
            context = {'message': 'Wrong OTP', 'class': 'danger', 'mobile': mobile}
            return render(request, 'login_otp.html', context)

    return render(request, 'login_otp.html', context)
