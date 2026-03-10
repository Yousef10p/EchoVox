from django.urls import path
from . import views

urlpatterns = [
    path('',                              views.browse,       name='translators_browse'),
    path('new/',                          views.create_post,  name='create_post'),
    path('<int:pk>/',                     views.post_detail,  name='post_detail'),
    path('<int:post_pk>/accept/<int:reply_pk>/', views.accept_reply, name='accept_reply'),
]
