from django.shortcuts import render, redirect
from django.http import HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from .models import UserName, Message, Comment
from .forms import signin_form, register_form, update_info_form, change_password_form
# Create your views here.

def getUserContext(id):
    print "In method"
    user = UserName.objects.get(id=id)
    userlst = UserName.objects.all()
    context = {
        'user' : user,
        'userlst' : userlst
    }
    return context

def index(req):
    return render(req, 'user_app/index.html')

def sign_in(req):
    if req.method == 'POST':
        form = signin_form(req.POST)
        if form.is_valid():
            print "Valid Sign In"
            postData = {
                'password' : form.cleaned_data['password'],
                'email' : form.cleaned_data['email']
                }
            user = UserName.objects.signin(postData)
            id = user['user'].id
            if user['user'].admin_level == 2:
                return HttpResponsePermanentRedirect(reverse('dashboard_admin', args=(id,)))
            else:
                return HttpResponsePermanentRedirect(reverse('dashboard', args=(id,)))
        else:
            context = {
                'signin_form' : form
            }
            return render(req, 'user_app/sign_in.html', context)
    else:
        context = {
            'signin_form' : signin_form()
        }
        return render(req, 'user_app/sign_in.html', context)

def register(req):
    if req.method == 'POST':
        form = register_form(req.POST)
        if form.is_valid():
            # print "Valid Registration"
            postData = {
                'first_name' : form.cleaned_data['first_name'],
                'last_name' : form.cleaned_data['last_name'],
                'email' : form.cleaned_data['email'],
                'password' : form.cleaned_data['password']
                }
            user = UserName.objects.register(postData)
            id = user['user'].id
            if user['user'].admin_level == 2:
                return HttpResponsePermanentRedirect(reverse('dashboard_admin', args=(id,)))
            else:
                return HttpResponsePermanentRedirect(reverse('dashboard', args=(id,)))
        else:
            context = {
                'register_form' : form
                }
            return render(req, 'user_app/register.html', context)
    else:
        context = {
            'register_form' : register_form()
            }
        return render(req, 'user_app/register.html', context)

def dashboard(req, id):
    print "Getting to dashboard"
    context = getUserContext(id)
    return render(req, 'user_app/dashboard.html', context)

def dashboardAdmin(req, id):
    print "Getting to dashboard"
    context = getUserContext(id)
    return render(req, 'user_app/dashboard.html', context)

def add_new(req, id):
    user = UserName.objects.get(id=id)
    if req.method == 'POST':
        form = register_form(req.POST)
        if form.is_valid():
            # print "Valid Registration"
            postData = {
                'first_name' : form.cleaned_data['first_name'],
                'last_name' : form.cleaned_data['last_name'],
                'email' : form.cleaned_data['email'],
                'password' : form.cleaned_data['password']
                }
            UserName.objects.register(postData)
            if user.admin_level == 2:
                return HttpResponsePermanentRedirect(reverse('dashboard_admin', args=(id,)))
            else:
                return HttpResponsePermanentRedirect(reverse('dashboard', args=(id,)))
        else:
            context = {
                'register_form' : form,
                'user' : user
                }
            return render(req, 'user_app/add_new.html', context)
    else:
        context = {
            'register_form' : register_form(),
            'user' : user
            }
        return render(req, 'user_app/add_new.html', context)

def edit_user(req, pid, id):
    user = UserName.objects.get(id=id)
    person = UserName.objects.get(id=pid)
    if req.method == 'POST':
        form = update_info_form(req.POST)
        if form.is_valid():
            postData = {
                'first_name' : form.cleaned_data['first_name'],
                'last_name' : form.cleaned_data['last_name'],
                'email' : form.cleaned_data['email'],
                'admin_level' : form.cleaned_data['admin_level']
                }
            UserName.objects.update_info(postData)
            if user.admin_level == 2:
                return HttpResponsePermanentRedirect(reverse('dashboard_admin', args=(id,)))
            else:
                return HttpResponsePermanentRedirect(reverse('dashboard', args=(id,)))
            # return render(req, 'user_app/edit_user.html', context)
        else:
            context = {
                'user' : user,
                'person' : person,
                'update_info_form' : form
                # 'update_password_form': update_password_form()
                }
            return render(req, 'user_app/edit_user.html', context)
    else:
        # updateInfo = update_info_form()
        updateInfo =  update_info_form(initial={
            'first_name': person.first_name,
            'last_name': person.last_name,
            'email': person.email})
        context = {
            'user' : user,
            'person' : person,
            'update_info_form' : updateInfo,
            'change_password_form': change_password_form()
            }
        return render(req, 'user_app/edit_user.html', context)

def change_password(req, pid, id):
    if req.method == 'POST':
        user = UserName.objects.get(id=id)
        person = UserName.objects.get(id=pid)
        if req.method == 'POST':
            form = change_password_form(req.POST)
            if form.is_valid():
                postData = {
                    'id' : person.id,
                    'password' : form.cleaned_data['password']
                    }
                UserName.objects.change_password(postData)
                if user.admin_level == 2:
                    return HttpResponsePermanentRedirect(reverse('dashboard_admin', args=(id,)))
                else:
                    return HttpResponsePermanentRedirect(reverse('dashboard', args=(id,)))
            else:
                updateInfo =  update_info_form(initial={
                    'first_name': person.first_name,
                    'last_name': person.last_name,
                    'email': person.email})
                context = {
                    'user' : user,
                    'person' : person,
                    'update_info_form' : updateInfo,
                    'change_password_form': form
                    }
                return render(req, 'user_app/edit_user.html', context)
    else:
        updateInfo =  update_info_form(initial={
            'first_name': person.first_name,
            'last_name': person.last_name,
            'email': person.email})
        context = {
            'user' : user,
            'person' : person,
            'update_info_form' : updateInfo,
            'change_password_form': change_password_form()
            }
        return render(req, 'user_app/edit_user.html', context)

def logoff(req):
    return redirect('/')
