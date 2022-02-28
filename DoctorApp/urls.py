import imp
from pickle import FROZENSET
from django.conf.urls import url
from django.urls import path, include
from DoctorApp import views
from .views import LoginView, RegisterView,UserView,LogoutView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    
    path('addpost',views.addpost),

    path('showpost',views.showpost),


    path('register',RegisterView.as_view()),

    path('',views.login),

    path('loginjwt',LoginView.as_view()),

    path('user',UserView.as_view()),

    path('logout',LogoutView.as_view()),

    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)