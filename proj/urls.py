from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	#url(r'^contact/$', views.contact, name='contact'),
	url(r'^contact/', views.contact, name='contact'),
	url(r'^skill/', views.ajax_skill_search, name='ajax_skill_search'),
]
