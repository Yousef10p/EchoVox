from django.shortcuts import render
from apps.translators.models import CommunityPost


def landing(request):
    recent_posts = CommunityPost.objects.filter(status='open').order_by('-created_at')[:6]
    return render(request, 'core/landing.html', {'recent_posts': recent_posts})
