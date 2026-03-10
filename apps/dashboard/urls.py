from django.urls import path
from . import views

urlpatterns = [
    path('',                              views.overview,           name='admin_overview'),
    path('users/',                        views.users_list,         name='admin_users'),
    path('users/<int:pk>/',               views.user_detail,        name='admin_user_detail'),
    path('users/<int:pk>/ban/',           views.user_toggle_ban,    name='admin_user_ban'),
    path('users/<int:pk>/staff/',         views.user_toggle_staff,  name='admin_user_staff'),
    path('users/<int:pk>/delete/',        views.user_delete,        name='admin_user_delete'),
    path('posts/',                        views.posts_list,         name='admin_posts'),
    path('posts/<int:pk>/delete/',        views.post_delete,        name='admin_post_delete'),
    path('posts/<int:pk>/status/',        views.post_change_status, name='admin_post_status'),
    path('replies/',                      views.replies_list,       name='admin_replies'),
    path('replies/<int:pk>/delete/',      views.reply_delete,       name='admin_reply_delete'),
    path('jobs/',                         views.jobs_list,          name='admin_jobs'),
    path('jobs/<int:pk>/delete/',         views.job_delete,         name='admin_job_delete'),
]
