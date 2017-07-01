from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^signin$', views.sign_in, name = 'sign_in'),
    url(r'^register$', views.register, name = 'register'),
    url(r'^dashboard/(?P<id>\d+)$', views.dashboard, name = 'dashboard'),
    url(r'^dashboard/admin/(?P<id>\d+)$', views.dashboardAdmin, name = 'dashboard_admin'),
    url(r'^users/new/(?P<id>\d+)$', views.add_new, name = 'add_new'),
    url(r'^users/edit/(?P<pid>\d+)/(?P<id>\d+)$', views.edit_user, name = 'edit_user'),
    url(r'^users/edit/password/(?P<pid>\d+)/(?P<id>\d+)$', views.change_password, name = 'change_password'),
    url(r'^$', views.logoff, name = 'log_off')
]
