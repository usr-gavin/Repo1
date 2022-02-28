import re
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

#jws restframework
from rest_framework.views import APIView


# Create your views here.

from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse

from DoctorApp.models import Patients
from DoctorApp.serializers import PatientSerializer

from django.core.files.storage import default_storage

@csrf_exempt
def addpost(request):
    #return HttpResponse("hello")
    return render(request,"DoctorApp/addpost.html")


@csrf_exempt
def showpost(request):
    #return HttpResponse("hello")
    patients = Patients.objects.all()
    context={'patients':patients}
    return render(request,"DoctorApp/showpost.html",context)

@csrf_exempt
def signin(request):
    #return HttpResponse("hello")
    if request.method=='POST':
        uid = request.POST['uname']
        pas = request.POST['psw']

        user=authenticate(username=uid, password=pas)
        if user is not None:
            login(request,user)
            name=user.first_name
            return HttpResponse("Login Successfully")
        else:
            return HttpResponse("user not found") 
    else:
        return HttpResponse("function not found") 
                
@csrf_exempt
def homepage(request):
    #return HttpResponse("hello")
    return render(request,"DoctorApp/homepage.html")
   


   #rest jws

from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import DoctorSerializer
from .models import Doctors

import jwt, datetime


# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = DoctorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save() #saving User profile
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        email = request.POST['uname']
        password = request.POST['psw']

        user = Doctors.objects.filter(email=email).first()
            
        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')#.decode('utf-8')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response


class UserView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = Doctors.objects.filter(id=payload['id']).first()
        serializer = DoctorSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response


#CUSTOM 

@csrf_exempt
def login(request):
    #return HttpResponse("hello")
    if request.method=='POST':
        uid = request.POST['uname']
        pas = request.POST['psw']

        user = Doctors.objects.filter(email=uid).first()
            
        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(pas):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')#.decode('utf-8')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }

        user=authenticate(username=uid, password=pas)
        if user is not None:
            login(request,user)
            name=user.first_name
            
            return render(request,"DoctorApp/homepage.html")
        else:
            return render(request,"DoctorApp/signin.html")
    else:
        return render(request,"DoctorApp/signin.html")