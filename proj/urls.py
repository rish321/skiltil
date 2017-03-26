from django.conf.urls import url

from . import views

from django.views.generic.base import RedirectView
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^contact/$', views.contact, name='contact'),
    url(r'^skill/(.*)/$', views.details, name='skill'),
    url(r'^teachers/', RedirectView.as_view(url='/')),
    # url(r'^sitemap\.xml$', TemplateView.as_view(template_name='proj/sitemap.xml', content_type='text/xml')),
    url(r'^thanks/', views.thanks, name='thanks'),
    # url(r'^skill/', views.ajax_skill_search, name='ajax_skill_search'),
    url(r'^skills/topic/(.*)/$', views.ajax_skills, name='ajax_skills'),
    url(r'^skill_topics/$', views.ajax_skill_topics, name='ajax_skill_topics'),
    url(r'^skills/(.*)/$', views.ajax_skills_predef, name='ajax_skills_predef'),
    url(r'^favicon.ico$', RedirectView.as_view(url=('/static/favicon.ico'), permanent=False), name="favicon"),
    # url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'registration/login.html'}),
    url(r'^accounts/login/$', auth_views.login, {'template_name': 'registration/login.html'}, name="login"),
    url(r'^accounts/logout/$', auth_views.logout, name="logout"),
    url(r'^profile-updated/', views.updated, name='updated'),
    url(r'^skill_lookup/$', views.skill_lookup, name="skill_lookup"),
]
