from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.db.models import Count, Q
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta

from apps.translators.models import CommunityPost, PostReply
from apps.translate.models import TranslationJob


def is_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

admin_required = user_passes_test(is_admin, login_url='login')


@login_required
@admin_required
def overview(request):
    now = timezone.now()
    week_ago = now - timedelta(days=7)

    stats = {
        'total_users':       User.objects.count(),
        'new_users_week':    User.objects.filter(date_joined__gte=week_ago).count(),
        'total_posts':       CommunityPost.objects.count(),
        'open_posts':        CommunityPost.objects.filter(status='open').count(),
        'total_replies':     PostReply.objects.count(),
        'total_jobs':        TranslationJob.objects.count(),
        'jobs_week':         TranslationJob.objects.filter(created_at__gte=week_ago).count(),
    }

    recent_users  = User.objects.order_by('-date_joined')[:8]
    recent_posts  = CommunityPost.objects.select_related('user').order_by('-created_at')[:8]
    recent_jobs   = TranslationJob.objects.select_related('user').order_by('-created_at')[:8]

    return render(request, 'dashboard/overview.html', {
        'stats': stats,
        'recent_users': recent_users,
        'recent_posts': recent_posts,
        'recent_jobs':  recent_jobs,
    })


# ── USERS ──────────────────────────────────────────────────────

@login_required
@admin_required
def users_list(request):
    q      = request.GET.get('q', '')
    role   = request.GET.get('role', '')
    status = request.GET.get('status', '')

    qs = User.objects.annotate(
        post_count=Count('posts', distinct=True),
        job_count=Count('translations', distinct=True),
    ).order_by('-date_joined')

    if q:
        qs = qs.filter(Q(username__icontains=q) | Q(email__icontains=q) |
                       Q(first_name__icontains=q) | Q(last_name__icontains=q))
    if role == 'admin':
        qs = qs.filter(is_staff=True)
    elif role == 'user':
        qs = qs.filter(is_staff=False)
    if status == 'active':
        qs = qs.filter(is_active=True)
    elif status == 'banned':
        qs = qs.filter(is_active=False)

    return render(request, 'dashboard/users.html', {
        'users': qs, 'q': q, 'role': role, 'status': status,
    })


@login_required
@admin_required
def user_detail(request, pk):
    u = get_object_or_404(User, pk=pk)
    posts = CommunityPost.objects.filter(user=u).order_by('-created_at')
    replies = PostReply.objects.filter(user=u).select_related('post').order_by('-created_at')
    jobs = TranslationJob.objects.filter(user=u).order_by('-created_at')[:20]
    return render(request, 'dashboard/user_detail.html', {
        'u': u, 'posts': posts, 'replies': replies, 'jobs': jobs,
    })


@login_required
@admin_required
def user_toggle_ban(request, pk):
    if request.method != 'POST':
        return redirect('admin_users')
    u = get_object_or_404(User, pk=pk)
    if u == request.user:
        messages.error(request, "You can't ban yourself.")
        return redirect('admin_user_detail', pk=pk)
    u.is_active = not u.is_active
    u.save()
    action = 'unbanned' if u.is_active else 'banned'
    messages.success(request, f"User @{u.username} has been {action}.")
    return redirect(request.POST.get('next', 'admin_users'))


@login_required
@admin_required
def user_toggle_staff(request, pk):
    if request.method != 'POST':
        return redirect('admin_users')
    u = get_object_or_404(User, pk=pk)
    if u == request.user:
        messages.error(request, "You can't change your own role.")
        return redirect('admin_user_detail', pk=pk)
    u.is_staff = not u.is_staff
    u.save()
    role = 'Admin' if u.is_staff else 'User'
    messages.success(request, f"@{u.username} is now {role}.")
    return redirect(request.POST.get('next', 'admin_user_detail'), pk=pk)


@login_required
@admin_required
def user_delete(request, pk):
    if request.method != 'POST':
        return redirect('admin_users')
    u = get_object_or_404(User, pk=pk)
    if u == request.user:
        messages.error(request, "You can't delete your own account.")
        return redirect('admin_user_detail', pk=pk)
    username = u.username
    u.delete()
    messages.success(request, f"User @{username} has been permanently deleted.")
    return redirect('admin_users')


# ── POSTS ──────────────────────────────────────────────────────

@login_required
@admin_required
def posts_list(request):
    q      = request.GET.get('q', '')
    status = request.GET.get('status', '')
    cat    = request.GET.get('cat', '')

    qs = CommunityPost.objects.select_related('user').annotate(
        reply_cnt=Count('replies', distinct=True)
    ).order_by('-created_at')

    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q) |
                       Q(user__username__icontains=q))
    if status:
        qs = qs.filter(status=status)
    if cat:
        qs = qs.filter(category=cat)

    return render(request, 'dashboard/posts.html', {'posts': qs, 'q': q, 'status': status, 'cat': cat})


@login_required
@admin_required
def post_delete(request, pk):
    if request.method != 'POST':
        return redirect('admin_posts')
    post = get_object_or_404(CommunityPost, pk=pk)
    title = post.title
    post.delete()
    messages.success(request, f'Post "{title[:50]}" deleted.')
    return redirect(request.POST.get('next', 'admin_posts'))


@login_required
@admin_required
def post_change_status(request, pk):
    if request.method != 'POST':
        return redirect('admin_posts')
    post = get_object_or_404(CommunityPost, pk=pk)
    new_status = request.POST.get('status')
    if new_status in ['open', 'in_progress', 'completed']:
        post.status = new_status
        post.save()
        messages.success(request, f'Post status updated to {new_status}.')
    return redirect(request.POST.get('next', 'admin_posts'))


# ── REPLIES ────────────────────────────────────────────────────

@login_required
@admin_required
def replies_list(request):
    q = request.GET.get('q', '')
    qs = PostReply.objects.select_related('user', 'post').order_by('-created_at')
    if q:
        qs = qs.filter(Q(body__icontains=q) | Q(user__username__icontains=q) |
                       Q(post__title__icontains=q))
    return render(request, 'dashboard/replies.html', {'replies': qs, 'q': q})


@login_required
@admin_required
def reply_delete(request, pk):
    if request.method != 'POST':
        return redirect('admin_replies')
    reply = get_object_or_404(PostReply, pk=pk)
    reply.delete()
    messages.success(request, 'Reply deleted.')
    return redirect(request.POST.get('next', 'admin_replies'))


# ── TRANSLATION JOBS ───────────────────────────────────────────

@login_required
@admin_required
def jobs_list(request):
    q    = request.GET.get('q', '')
    jtype = request.GET.get('type', '')

    qs = TranslationJob.objects.select_related('user').order_by('-created_at')
    if q:
        qs = qs.filter(Q(user__username__icontains=q) | Q(original_text__icontains=q) |
                       Q(translated_text__icontains=q))
    if jtype:
        qs = qs.filter(job_type=jtype)

    return render(request, 'dashboard/jobs.html', {'jobs': qs, 'q': q, 'jtype': jtype})


@login_required
@admin_required
def job_delete(request, pk):
    if request.method != 'POST':
        return redirect('admin_jobs')
    job = get_object_or_404(TranslationJob, pk=pk)
    job.delete()
    messages.success(request, 'Translation job deleted.')
    return redirect(request.POST.get('next', 'admin_jobs'))
