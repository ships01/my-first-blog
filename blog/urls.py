from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.post_main, name='post_main'),
    url(r'^url/(?P<pk>\S+)/$', views.post_url, name='post_url'),
    url(r'^js/(?P<pk>[a-z.0-9]+)/$', views.post_any, name='post_any'),
    url(r'^login/$', views.LoginFormView.as_view(), name='post_login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='post_logout'),
    url(r'^register/$', views.RegisterFormView.as_view(), name='post_reg'),

    url(r'^post/$', views.post_list, name='post_list'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/(?P<pk>\d+)/(?P<ps>\d+)/$', views.post_detail2, name='post_detail2'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
]