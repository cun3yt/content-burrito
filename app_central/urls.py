from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^burrito$', views.create_burrito, name='burrito'),
    url(r'^banner-builder$', views.banner_builder, name='banner-builder'),
    url(r'^update-burrito$', views.update_burrito, name='update-burrito'),
    url(r'^get-burrito-url$', views.get_burrito_url, name='burrito-url'),
    url(r'^b', views.serve_burrito, name='burrito'),
    url(r'^$', views.index, name='index'),
]
