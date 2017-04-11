"""projectX URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap

from proj.models import SkillSitemap

urlpatterns = [
	url(r'^', include('proj.urls')),
	url(r'^sitemap\.xml$', sitemap, {'sitemaps': {'skill': SkillSitemap}}, name='django.contrib.sitemaps.views.sitemap'),
	#url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': {'skill', SkillSitemap}}),
	url(r'^admin/', admin.site.urls),
	url(r'^session/', include('session.urls')),
	url(r'^profile/', include('customers.urls')),
	url(r'^tinymce/', include('tinymce.urls')),
	url(r'^accounts/', include('allauth.urls')),
	url(r'^adminactions/', include('adminactions.urls')),
]
