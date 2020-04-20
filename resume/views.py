from django.shortcuts import render, redirect
from django.views import View
from resume.models import Resume
from vacancy.models import Vacancy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.http import HttpResponseForbidden
from django import forms


class DescriptionForm(forms.Form):
    text = forms.CharField(label='description')

# Create your views here.

class MenuView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "hyperjob/menu.html")

class ResumeView(View):
    def get(self, request, *args, **kwargs):
        resumes = Resume.objects.all()
        return render(request, "hyperjob/resumes.html", {'resumes':resumes})

class MyLoginView(LoginView):
    form_class = AuthenticationForm
    redirect_authenticated_user = True
    template_name = 'hyperjob/login.html'

class MySignupView(CreateView):
   form_class = UserCreationForm
   success_url = 'login'
   template_name = 'hyperjob/signup.html'

class HomeView(View):
    def get(self, request, *args, **kwargs):
        df1 = DescriptionForm()
        return render(request, "hyperjob/home.html",  {'df1':df1})
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff:
                if 'vacancy' in request.POST:
                    df = DescriptionForm(request.POST)
                    if df.is_valid():
                        v = df.cleaned_data['text']
                        new_v = Vacancy.objects.create(author=request.user, description=v)
                        new_v.save()
                    return redirect('vacancy/new')
                else:
                    return HttpResponseForbidden()
            else:
                if 'resume' in request.POST:
                    df = DescriptionForm(request.POST)
                    if df.is_valid():
                        r = df.cleaned_data['text']
                        new_r = Resume.objects.create(author=request.user, description=r)
                        new_r.save()
                    return redirect('resume/new')
                else:
                    return HttpResponseForbidden()
        else:
            return HttpResponseForbidden()

class NewResumeView(View):
    def get(self, request, *args, **kwargs):
        resume = Resume.objects.filter(author=request.user).last()
        return render(request, "hyperjob/new_resume.html", {'resume':resume.description})




