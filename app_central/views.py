from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.middleware.csrf import get_token
from .models import Burrito, BetaSubscriber
from .forms import SignupForm, LoginForm
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from ipware.ip import get_real_ip
from django.db import IntegrityError

import logging
import daiquiri

daiquiri.setup(level=logging.INFO)
logger = daiquiri.getLogger()


def index(request):
    if not request.COOKIES.get('pass_lp', False):
        return render(request, 'landing_page.html', context={'csrf_token': get_token(request)})

    return render(request, 'home.html', context={})


def beta_subscribe(request):
    ip = get_real_ip(request)

    if not (request.method == "POST"):
        error_msg = "Wrong HTTP Method"
        logger.info("{error_msg} for IP: {ip}".format(error_msg=error_msg, ip=ip))
        response = JsonResponse({"result": "error", "error_message": error_msg})
        response.status_code = 405
        return response

    email = request.POST.get('email')

    try:
        validate_email(email)
    except ValidationError:
        error_msg = "Email address is malformed. Please try a valid address"
        logger.info("{error_msg} for IP: {ip}, Email: {email}".format(error_msg=error_msg, ip=ip, email=email))
        response = JsonResponse({"result": "error", "error_message": error_msg})
        response.status_code = 400
        return response

    try:
        subscriber = BetaSubscriber(email=email, ip=ip)
        subscriber.save()
        logger.info("Successful save for IP: {ip}, email: {email}".format(ip=ip, email=email))
    except IntegrityError:
        logger.info("Integrity Error for Beta Subscriber IP: {ip}, Email: {email}".format(ip=ip, email=email))

    response = JsonResponse({"result": "success"})
    response.status_code = 200
    return response


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


def landing_page(request):
    return render(request, 'landing_page.html')
