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
    url(r'^users/show/(?P<pid>\d+)/(?P<id>\d+)$', views.user_page, name = 'user_page'),
    url(r'^users/delete/(?P<pid>\d+)/(?P<id>\d+)$', views.remove, name = 'remove'),
    url(r'^users/(?P<pid>\d+)/(?P<id>\d+)/message$', views.add_message, name = 'add_message'),
    url(r'^users/(?P<pid>\d+)/(?P<mid>\d+)/(?P<id>\d+)/comment$', views.add_comment, name = 'add_comment'),
    url(r'^$', views.logoff, name = 'log_off')
]
