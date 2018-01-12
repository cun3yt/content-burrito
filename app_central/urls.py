from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^burrito$', views.create_burrito, name='burrito'),
    url(r'^banner-builder$', views.banner_builder, name='banner-builder'),
    url(r'^update-burrito$', views.update_burrito, name='update-burrito'),
    url(r'^get-burrito-url$', views.get_burrito_url, name='burrito-url'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^beta-subscribe$', views.beta_subscribe, name='beta-subscribe'),
    url(r'^b$', views.serve_burrito, name='burrito'),
    url(r'^landing-page$', views.landing_page, name='landing-page'),
    url(r'^$', views.index, name='index'),
]
