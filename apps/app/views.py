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

def create_user(request):
    print(request.POST)
    request.session['errors'] = []
    data_is_valid, errors = User.objects.validate(request.POST)
    print ('data is valid',data_is_valid)
    print (errors)
    if  data_is_valid:    
        loginreg = User.objects.create(
            first_name=request.POST["first_name"],
            last_name=request.POST["last_name"],
            email=request.POST["email"],
            password = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()),
        )
        request.session['first_name']=request.POST['first_name']
        request.session['last_name']=request.POST['last_name']
        request.session['email']=request.POST['email']
    
        return redirect('/shows')
    else:
        request.session["errors"]=errors
        return redirect('/')

def login(request):
    request.session['errors'] = []
    user = User.objects.filter(email=request.POST['email'])
    this_user = user.first()
    if len(user) > 0:
        print(request.POST['password'])
        for key in user.__dict__.keys():
            print(key)
        if bcrypt.checkpw(request.POST['password'].encode(), this_user.password.encode()):
            request.session['email'] = request.POST['email']
            request.session['first_name']=this_user.first_name
            print("password match")
            return redirect("/home")
        else:
            error,invalid=User.objects.create_error_message(label="login", message="Invalid credentials")
            errors=[error]
            request.session["errors"]=errors
            print("failed password") 
            return redirect('/')
    else:
        error,invalid=User.objects.create_error_message(label="login", message="Invalid credentials")
        errors=[error]
        request.session["errors"]=errors
        return redirect("/")

def logout(request):
    del request.session["email"]
    return redirect("/")

def success(request):
    shows = Show.objects.all().order_by("-created_at")[:5]
    user = User.objects.get( email = request.session["email"])
    ratings = Rating.objects.filter(user_id = user.id).order_by("-rating")[:5]
    context = {
        "user":user,
        "shows":shows,
        "ratings":ratings,
    }
    return render(request, 'app/home.html', context)

def create_show(request):
    shows = Show.objects.all().order_by("-created_at")[:5]
    user = User.objects.get( email = request.session["email"])
    ratings = Rating.objects.filter(user_id = user.id)
    context = {
        "user":user,
        "shows":shows,
        "ratings":ratings,
    }
    print(request.POST)
    return render(request, "app/add_show.html",context)

def add_show(request):
    errors = Show.objects.basic_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            print(key, value)
            messages.error(request, value)
        return redirect("/shows/new")
    else:
        show = Show.objects.create(
            name = request.POST["name"],
            network = request.POST["network"]
        )
        return redirect("/home")

def view_show(request, id):
    ratings = Rating.objects.filter(show_id=id).order_by("-created_at")
    show = Show.objects.get(id=id)
    user = User.objects.get(email = request.session["email"])
    user_rating = Rating.objects.filter(show_id = id, user_id = user.id)
    context = {
        "show":show,
        "ratings":ratings,
        "user":user,
        "user_rating":user_rating,
    }
    return render(request, "app/view_show.html", context)