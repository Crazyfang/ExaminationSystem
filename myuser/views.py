from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
import json
from .form import UserForm, UserFormRegister
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url

# Create your views here.


def login_view(request):
    if request.method == 'GET':
        hash_key = CaptchaStore.generate_key()
        image_url = captcha_image_url(hash_key)
        return render(request, 'myuser/login.html', {'hash_key': hash_key, 'image_url': image_url})
    else:
        user = UserForm(request.POST)

        if user.is_valid():
            login_user = authenticate(**user.cleaned_data)
            # Correct password, and the user is marked "active"
            login(request, login_user)
            data = {'state': 'success'}
            # Redirect to a success page.
            return HttpResponse(json.dumps(data))
            # return redirect("/user/index")
        else:
            data = {'state': 'fail'}
            return HttpResponse(json.dumps(data))
            # return redirect("/user/login")


def register_view(request):
    if request.method == 'GET':
        hash_key = CaptchaStore.generate_key()
        image_url = captcha_image_url(hash_key)
        forms = UserFormRegister()
        return render(request, 'myuser/reg.html', {'hash_key': hash_key, 'image_url': image_url, 'forms': forms})
    elif request.method == 'POST':
        user = UserFormRegister(request.POST)
        data = {'state': 'success', 'url': reverse('user:login')}

        if user.is_valid():
            new_user = user.save(commit=False)
            new_user.set_password(user.cleaned_data['password'])
            new_user.save()
            return HttpResponse(json.dumps(data))

        else:
            data = {'state': 'fail', 'msg': user.errors}
            return HttpResponse(json.dumps(data))


@login_required()
def index_view(request):
    print(request.user.department)
    print(request.user.user_code)

    return render(request, 'myuser/index.html')

