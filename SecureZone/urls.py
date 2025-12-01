"""SecureZone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from SecureZone_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.Login),
    path('Login_post', views.Login_post),
    path('Logout', views.Logout),
    path('AddSecurity',views.AddSecurity),
    path('ViewSecurity',views.ViewSecurity),
    path('delete_security/<id>',views.delete_security),
    path('Edit/<id>',views.Edit),
    path('Assign/<id>',views.Assign),
    path('ViewTask/<id>',views.ViewTask),
    path('SendAlert',views.SendAlert),
    path('ViewAlert',views.ViewAlert),
    path('ViewCmplnt',views.ViewCmplnt),
    path('AdminHome',views.AdminHome),
    path('Addsecurity_post',views.Addsecurity_post),
    path('Edit_post/<id>',views.Edit_post),
    path('Assign_post/<id>',views.Assign_post),
    path('ViewReport/<id>',views.ViewReport),
    path('SendAlert_post',views.SendAlert_post),
    path('Reply/<id>',views.Reply),
    path('Reply_post/<id>',views.Reply_post),
    path('send_complaint_post',views.send_complaint_post),
    path('send_report_post',views.send_report_post),

    #======================================================================================================================


    path('and_login',views.and_login),
    path('and_manage_profile',views.and_manage_profile),
    path('and_view_task',views.and_view_task),
    path('and_view_response',views.and_view_response),
    path('and_alert',views.and_alert),
    path('update_post',views.update_post),
    path('notification',views.notification),
    path('', views.index),


]
