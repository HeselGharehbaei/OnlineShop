from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegistrationForm, VerifyCodeForm, UserLoginForm
import random
from utils import send_otp_code
from .models import OtpCode, User
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import authenticate, login, logout


class UserRegisterView(View):
    form_class= UserRegistrationForm
    register_template= 'accounts/register.html'

    def get(self, request):
        form= self.form_class
        return render(request, self.register_template, {'form':form})
    def post(self, request):
        form= self.form_class(request.POST)
        if form.is_valid():
            random_code= random.randint(1000, 9999)
            send_otp_code(form.cleaned_data['phone_number'], random_code)
            OtpCode.objects.create(phone_number= form.cleaned_data['phone_number'], code= random_code)
            request.session['user_registration_info']= {
                'phone_number': form.cleaned_data['phone_number'],
                'email': form.cleaned_data['email'],
                'full_name': form.cleaned_data['full_name'],
                'password': form.cleaned_data['password']
            }
            messages.success(request, 'we send you a code', 'success')
            return redirect('accounts:verify_code')
        return render(request, self.register_template, {'form':form})


class UserRegisterVerifyCodeView(View):
    form_class= VerifyCodeForm
    registeration_form= UserRegistrationForm

    def get(self, request):
        form= self.form_class
        return render(request, 'accounts/verify.html', {'form': form})
    def post(self, request):
        user_session= request.session['user_registration_info']
        code_instance= OtpCode.objects.get(phone_number= user_session['phone_number'])
        code_expired_time= code_instance.created + timedelta(minutes=1)
        now= timezone.now()
        form= self.form_class(request.POST)
        if form.is_valid():
            cd= form.cleaned_data
            if cd['code']== code_instance.code:
                if now<=code_expired_time:               
                    User.objects.create_user(user_session["phone_number"], user_session["email"], 
                                            user_session["full_name"], user_session["password"])
                    code_instance.delete()
                    messages.success(request, "you registred", 'success')
                    return redirect('home:home')
                else:
                    code_instance.delete()
                    messages.error(request, "this code is expired try again", 'danger')
                    return redirect('accounts:user_register')
            else:
                messages.error(request, "this code is wrong", 'danger')
                return redirect('accounts:verify_code')
        return redirect('home:home')    
    

class UserLoginView(View):
    form_class= UserLoginForm
    login_tempelate= 'accounts/login.html'

    def get(self, request):
        form= self.form_class
        return render(request, self.login_tempelate, {'form': form})
    
    def post(self, request):
        form= self.form_class(request.POST)
        if form.is_valid():
            login_data= form.cleaned_data
            user= authenticate(phone_number= login_data['phone_number'], password= login_data['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'logging in successfully', 'success')
                return redirect('home:home')
            else:
                messages.error(request, 'phone number or password is wrong', 'danger')
        return render(request, self.login_tempelate, {'form':form})   


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'logging out successfully', 'success')
        return redirect("home:home")              
