from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.show_profile, name='show_profile'),
	url(r'^update_skills/$', views.update_skills, name='update_skills'),
]
