from django.conf.urls import url

from . import views

from django.views.generic.base import RedirectView
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView



urlpatterns = [
	url(r'^$', views.index, name='index'),
	#url(r'^contact/$', views.contact, name='contact'),
	url(r'^skill/(.*)/$', views.details, name='skill'),
	url(r'^teachers/', RedirectView.as_view(url='/')),
	url(r'^sitemap\.xml$', TemplateView.as_view(template_name='proj/sitemap.xml', content_type='text/xml')),
	url(r'^thanks/', views.thanks, name='thanks'),
	#url(r'^skill/', views.ajax_skill_search, name='ajax_skill_search'),
	url(r'^skills/topic/(.*)/$', views.ajax_skills, name='ajax_skills'),
	url(r'^skill_topics/$', views.ajax_skill_topics, name='ajax_skill_topics'),
	url(r'^skills/(.*)/$', views.ajax_skills_predef, name='ajax_skills_predef'),
	url(r'^favicon.ico$', RedirectView.as_view(url=('/static/favicon.ico'), permanent=False), name="favicon"),
]
