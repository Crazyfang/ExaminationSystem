from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
import json
from .form import UserForm
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
        print(request.POST)

        user_code = request.POST.get('user_code', '')
        password = request.POST.get('password', '')
        print(user.is_valid())
        print(user.cleaned_data)
        print(user.errors)
        user = authenticate(user_code=user_code, password=password)
        if user is not None and user.is_active:
            # Correct password, and the user is marked "active"
            login(request, user)
            data = {'state': 'success'}
            # Redirect to a success page.
            return HttpResponse(json.dumps(data))
            # return redirect("/user/index")
        else:
            data = {'state': 'fail'}
            return HttpResponse(data)
            # return redirect("/user/login")


@login_required()
def index_view(request):
    print(request.user.user_code)
    print(request.user)

    return render(request, 'myuser/index.html')

