from django.urls import path
from . import views

urlpatterns = [
    path('', views.translate_home, name='translate_home'),
    path('history/', views.history, name='translate_history'),
    path('history/<int:pk>/', views.job_detail, name='translate_job_detail'),
    path('api/text/', views.translate_text_api, name='translate_text_api'),
    path('api/file/', views.translate_file_api, name='translate_file_api'),
    path('api/video-url/', views.translate_video_url_api, name='translate_video_url_api'),
    path('api/video-upload/', views.translate_video_upload_api, name='translate_video_upload_api'),
]
