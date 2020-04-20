from django.shortcuts import render
from django.views import View
from vacancy.models import Vacancy
# Create your views here.
class VacancyView(View):
    def get(self, request, *args, **kwargs):
        vacancies = Vacancy.objects.all()
        return render(request, "hyperjob/vacancies.html", {'vacancies': vacancies})

class NewVacancyView(View):
    def get(self, request, *args, **kwargs):
        vacancy = Vacancy.objects.filter(author=request.user).last()
        return render(request, "hyperjob/new_vacancy.html", {'vacancy':vacancy.description})

