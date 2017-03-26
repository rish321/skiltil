from django.contrib import sitemaps
import datetime

from django.urls import reverse


class Sitemap(sitemaps.Sitemap):

    def changefreq(self, obj):
        return 'weekly'

    def lastmod(self, obj):
        return datetime.datetime.now()

    def location(self, obj):
        return reverse(obj)