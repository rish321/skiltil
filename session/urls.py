from django.conf.urls import url

from . import views

urlpatterns = [
	#url(r'^$', views.index, name='index'),
	#url(r'^call/', views.call, name='call'),
	url(r'^invoice/([0-9]+)/$', views.call_invoice, name='call_invoice'),	
	#url(r'^teachers/', views.teachers, name='teachers'),
	#url(r'^skill/', views.ajax_skill_search, name='ajax_skill_search'),
	#url(r'^favicon.ico$', RedirectView.as_view(url=('/static/favicon.ico'), permanent=False), name="favicon"),
]
