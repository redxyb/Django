from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

# Create your views here.
def kobe(request):
    return render(request, 'kobe.html')