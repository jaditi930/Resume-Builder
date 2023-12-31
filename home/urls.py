from django.contrib import admin
from django.urls import path,include
from home import views

urlpatterns = [
path("",views.index,name="home"),
path("log_out",views.log_out,name="log_out"),
path("login",views.login_user,name="login_user"),
path("login_user_form",views.login_form,name="login_form"),
path("signup",views.create_user,name="create"),
path("create_user_form",views.create_user_form,name="create_form"),
path("contact_us",views.contact_us,name="contact_us"),
path("submit_contact_form",views.submit_contact_form,name="submit_contact_form"),
path("generate_data",views.generate_data,name="generate_data"),
path("generate_data_form",views.generate_data_form,name="generate_data_form"),
path("show_resume",views.show_resume),
path("edit_resume",views.edit_resume),
path("edit_resume_form",views.edit_resume_form),
]
