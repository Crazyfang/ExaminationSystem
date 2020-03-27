from django.shortcuts import render
# from django.views.decorators.clickjacking import xframe_options_exempt

# Create your views here.


def index_view(request):
    return render(request, 'home/index.html')


def console_view(request):
    return render(request, 'home/console.html')
