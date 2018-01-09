from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.db import transaction
from django.contrib.auth.decorators import login_required
from .models import Burrito
from .forms import SignupForm, LoginForm

@csrf_exempt
def index(request):
    return render(request, 'home.html', context={})


def banner_builder(request):
    id = request.GET.get('id')
    burrito = Burrito.objects.get(id=id)
    context = {
        'id': id,
        'burrito': burrito
    }
    return render(request, 'banner_builder.html', context=context)


@csrf_exempt
def create_burrito(request):
    url = request.POST.get('url')
    thumbnail = request.POST.get('thumbnail')
    source = request.POST.get('source')

    burrito = Burrito(url=url, thumbnail_url=thumbnail, source=source)
    burrito.save()

    return JsonResponse({
        'id': str(burrito.id)
    })


@csrf_exempt
def update_burrito(request):
    id = request.POST.get('id')
    banner_url = request.POST.get('banner_url')
    banner_message = request.POST.get('banner_message')
    banner_color_scheme = request.POST.get('banner_color_scheme')

    with transaction.atomic():
        burrito = Burrito.objects.get(id=id)
        burrito.banner_url = banner_url
        burrito.banner_message = banner_message
        burrito.banner_color_scheme = banner_color_scheme
        burrito.save()

    return JsonResponse({
        'id': str(burrito.id)
    })


@login_required(login_url='login')
def get_burrito_url(request):
    id = request.GET.get('id')
    burrito = Burrito.objects.get(id=id)
    context = {
        'burrito': burrito
    }
    return render(request, 'burrito_url.html', context=context)


def serve_burrito(request):
    id = request.GET.get('id')
    burrito = Burrito.objects.get(id=id)
    from urllib.parse import unquote
    url = unquote(burrito.url)
    return render(request, 'burrito.html', context={'burrito': burrito, 'url': url})


def signup(request):
    if request.user.is_authenticated:
        return JsonResponse({'id': "ALready authenticated {}".format(request.user.email)})

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignupForm()
    return render(request, 'signup.html', context={'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return JsonResponse({'id': "ALready authenticated {}".format(request.user.email)})

    if request.method == "POST":
        form = LoginForm(request=request, data=request.POST.dict())

        if form.is_valid():
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = LoginForm()

    context = {'form': form}

    if request.GET.get('next'):
        context['next'] = next

    # import ipdb
    # ipdb.set_trace()

    return render(request, 'login.html', context=context)
