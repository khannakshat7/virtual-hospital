from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as log_out
from django.conf import settings
from django.http import HttpResponseRedirect
from urllib.parse import urlencode
from auth0login.forms import UserForm
from django.contrib.auth import authenticate, login, logout
from auth0login.models import appointment
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json


def index(request):
    user = request.user
    if user.is_superuser:
        return redirect('/doclogin')
    elif user.is_authenticated:
        return redirect(dashboard)
    else:
        return render(request, 'index.html')

def doctorRegister(request):
    registeredcheck = False
    if(request.method == 'POST'):
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.is_staff = True
            user.is_superuser = True
            user.save()
            registeredcheck = True
            msg={"message":True}
            return render(request,"login.html",msg)
        else:
            error={"error":True}
            return render(request,"register.html",error)
    else:
        return render(request, 'register.html')

@csrf_exempt
def doctorLogin(request):
    if(request.method == 'POST'):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_superuser or user.is_active:
                login(request,user)

                appointmentDetails = list(appointment.objects.filter(doctorName=username))
                appoint=[]
                for i in range(len(appointmentDetails)):
                    appoint.insert(0,{
                    "id" : appointmentDetails[i].appointmentid,
                    "username" : appointmentDetails[i].username,
                    "doctorName" : appointmentDetails[i].doctorName,
                    "status" : appointmentDetails[i].status,
                    "date" : appointmentDetails[i].created_at,
                    "Report":appointmentDetails[i].prevReport,
                    "scans":appointmentDetails[i].prevScans})

                data = {
                    "appoint":appoint
                }

                return render(request,"doctordash.html",data)
            else:
                return render(request,"login.html",{"err":True})
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return render(request,"login.html",{"invalid":True})
    else:
        return render(request, 'login.html')     

@login_required
def dashboard(request):
    user = request.user
    auth0user = user.social_auth.get(provider='auth0')

    appointmentDetails = list(appointment.objects.all())
    appoint=[]
    for i in range(len(appointmentDetails)):
        appoint.insert(0,{
        "id" : appointmentDetails[i].appointmentid,
        "doctorName" : appointmentDetails[i].doctorName,
        "status" : appointmentDetails[i].status,
        "date" : appointmentDetails[i].created_at,
        "Report":appointmentDetails[i].prevReport,
        "scans":appointmentDetails[i].prevScans,
        "medicines":appointmentDetails[i].medicines,
        "tests":appointmentDetails[i].tests,
        "summary":appointmentDetails[i].summery})

    data = {
        "appoint":appoint
    }
    return render(request, 'dashboard.html', {
        'auth0User': auth0user,
        "data":data
    })

def logoutp(request):
    log_out(request)
    return_to = urlencode({'returnTo': request.build_absolute_uri('/')})
    logout_url = 'https://%s/v2/logout?client_id=%s&%s' % \
                 (settings.SOCIAL_AUTH_AUTH0_DOMAIN, settings.SOCIAL_AUTH_AUTH0_KEY, return_to)
    return HttpResponseRedirect(logout_url)

@login_required
@csrf_exempt
def appointmentpatient(request):
    if request.method == 'POST' and request.FILES['prevReport'] and request.FILES['prevScans']:
        instance = appointment()
        instance.username = request.user.username
        instance.doctorName = request.POST['doctorname']
        instance.prevReport = request.FILES['prevReport']
        instance.prevScans = request.FILES['prevScans']
        instance.save()
        return redirect(dashboard)
    else:
        doctors = list(User.objects.filter(is_superuser=True))
        return render(request, "appointment.html",{"doctors":doctors})

@csrf_exempt
def done(request):
    appointmentid = request.POST["id"]
    appointment.objects.filter(appointmentid=appointmentid).update(
    status = True,
    medicines = request.POST["medicines"],
    tests = request.POST["tests"],
    summery = request.POST["summary"])
    msg={"success":True}
    return render(request,"login.html",msg)