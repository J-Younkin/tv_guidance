from django.shortcuts import render, redirect
from django.contrib import messages
from . models import *
import bcrypt

def index(request):
    if "errors" in request.session:
        errors = request.session["errors"]
        del request.session["errors"]
    else:
        errors = []
        
    context = {
        "errors": errors
    }
    return render(request, 'app/index.html', context)