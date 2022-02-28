from django.contrib import admin

from django.urls import path
from django.views.generic import TemplateView
from django.conf.urls import url,include

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('',TemplateView.as_view(template_name='index.html')),
    url('log/',include('DoctorApp.urls'))
]
