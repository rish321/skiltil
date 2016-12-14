from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	#url(r'^contact/$', views.contact, name='contact'),
	url(r'^contact/', views.contact, name='contact'),
	#url( r'^skills/$', views.ajax_user_search, name = 'demo_user_search' ),
]
