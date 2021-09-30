from django.http.response import HttpResponse
from django.template import loader
from single_pages.models import User
from django.shortcuts import render, redirect
from notice.models import Notice
from django. contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from argon2 import PasswordHasher, exceptions

def landing(request):
    recent_notices = Notice.objects.order_by('-pk')[:3]
    return render(
        request, 
        'single_pages/landing.html',
        {
            'recent_notices': recent_notices,
        }
    )

    
def about_me(requset):
    return render(
        requset, 
        'single_pages/about_me.html'
    )

def loginview (request):
    return render(request, 'single_pages/login.html')

def loginprocess (request):
    try:
        user = User.objects.get(user_id=request.POST['E-mail'])
        PasswordHasher().verify(user.user_password, request.POST['password1'])
        request.session['loginuser'] = user.user_name
        request.session['usermail'] = user.user_id
        request.session['userpoint'] = user.user_point

    except exceptions.VerifyMismatchError:
        return render(request, 'single_pages/login.html', {
            'error_message' : "회원정보가 없거나 잘못 입력하셨습니다.",
        })

    except (KeyError, User.DoesNotExist):
        return render(request, 'single_pages/login.html', {
            'error_message' : "회원정보가 없거나 잘못 입력하셨습니다.",
        })
        
    
    return redirect('home') 

def signup(request):
    if request.method == 'POST': 
        print(request.POST )
        if request.POST['password1'] == request.POST['password2']:
            user = User(user_id= request.POST['E-mail'], user_name = request.POST['username'], user_password=PasswordHasher().hash(request.POST['password1']))
            user.save()
            #auth.login(request, user)
            return redirect('loginview')
    else:
        return render(request, 'single_pages/signup.html')

def logout(request):
    if request.session.get('loginuser'):  
        del(request.session['loginuser']) 
    if request.session.get('userpoint'):   
        del(request.session['userpoint']) 
    return redirect('home')

def pwResetview (request):
    return render(request, 'single_pages/pw_reset.html')

def passwordReset(request):
    try:
        if request.method == 'POST': 
            user = User.objects.get(user_id= request.POST['E-mail'])
            if request.POST['new_pw1'] == request.POST['new_pw2']:
                user.user_password = PasswordHasher().hash(request.POST['new_pw1'])
                user.save()
                return redirect('loginview')
    except (KeyError, User.DoesNotExist):
        return render(request, 'single_pages/pw_reset.html', {
            'error_message' : "회원정보가 없거나 잘못 입력하셨습니다.",
        })

@csrf_exempt
def forw_point(request):
    user = User.objects.get(user_name=request.session['loginuser'])
    request.session['userpoint'] = user.user_point
    receive_message = request.POST.get('userpoint')
    minus_point = 1000
    send_message = {'userpoint' : user.user_point - minus_point}
    user.user_point = user.user_point - minus_point
    user.save()
    return JsonResponse(send_message)
# Create your views here.

@csrf_exempt
def view_point(request):
    user = User.objects.get(user_name=request.session['loginuser'])
    receive_message = request.POST.get('userpoint')
    send_message = {'userpoint' : user.user_point}
    return JsonResponse(send_message)

@csrf_exempt
def corr_point(request):
    user = User.objects.get(user_name=request.session['loginuser'])
    request.session['userpoint'] = user.user_point
    receive_message = request.POST.get('userpoint')
    plus_point = 1000
    send_message = {'userpoint' : user.user_point + plus_point}
    user.user_point = user.user_point + plus_point
    user.save()
    return JsonResponse(send_message)

@csrf_exempt
def view_name(request):
    user = User.objects.get(user_name=request.session['loginuser'])
    receive_message = request.POST.get('username')
    send_message = {'username' : user.user_name}
    return JsonResponse(send_message)

@csrf_exempt
def view_id(request):
    user = User.objects.get(user_name=request.session['loginuser'])
    receive_message = request.POST.get('userid')
    send_message = {'userid' : user.user_id}
    return JsonResponse(send_message)