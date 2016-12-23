from django.conf.urls import url

from . import views

from django.views.generic.base import RedirectView


urlpatterns = [
	url(r'^$', views.index, name='index'),
	#url(r'^contact/$', views.contact, name='contact'),
	url(r'^contact/', views.contact, name='contact'),
	url(r'^teachers/', views.teachers, name='teachers'),
	url(r'^skill/', views.ajax_skill_search, name='ajax_skill_search'),
	url(r'^favicon.ico$', RedirectView.as_view(url=('/static/favicon.ico'), permanent=False), name="favicon"),
]
