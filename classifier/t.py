from django.http import HttpResponse
from django.shortcuts import render
def home1(request):
    return render(request, 'pfa/templateshome.html')
