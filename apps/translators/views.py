from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CommunityPost, PostReply, LANGUAGE_CHOICES, CATEGORY_CHOICES
from .forms import PostForm, ReplyForm


def browse(request):
    qs = CommunityPost.objects.all()

    lang_filter = request.GET.get('lang', '')
    cat_filter  = request.GET.get('cat', '')
    status_filter = request.GET.get('status', '')
    search      = request.GET.get('q', '')

    if lang_filter:
        qs = qs.filter(source_lang=lang_filter) | CommunityPost.objects.filter(target_lang=lang_filter)
    if cat_filter:
        qs = qs.filter(category=cat_filter)
    if status_filter:
        qs = qs.filter(status=status_filter)
    if search:
        qs = qs.filter(title__icontains=search) | CommunityPost.objects.filter(description__icontains=search)

    qs = qs.order_by('-created_at').distinct()

    return render(request, 'translators/browse.html', {
        'posts':       qs,
        'languages':   dict(LANGUAGE_CHOICES),
        'categories':  dict(CATEGORY_CHOICES),
        'lang_filter': lang_filter,
        'cat_filter':  cat_filter,
        'status_filter': status_filter,
        'search_query': search,
    })


def post_detail(request, pk):
    post = get_object_or_404(CommunityPost, pk=pk)
    post.views += 1
    post.save(update_fields=['views'])

    reply_form = ReplyForm()
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to reply.')
            return redirect('login')
        reply_form = ReplyForm(request.POST)
        if reply_form.is_valid():
            reply = reply_form.save(commit=False)
            reply.post = post
            reply.user = request.user
            reply.save()
            messages.success(request, 'Your reply was posted!')
            return redirect('post_detail', pk=pk)

    return render(request, 'translators/post_detail.html', {
        'post': post,
        'replies': post.replies.all(),
        'reply_form': reply_form,
    })


@login_required
def create_post(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        post.save()
        messages.success(request, 'Your translation request was posted!')
        return redirect('post_detail', pk=post.pk)
    return render(request, 'translators/create_post.html', {'form': form})


@login_required
def accept_reply(request, post_pk, reply_pk):
    post  = get_object_or_404(CommunityPost, pk=post_pk, user=request.user)
    reply = get_object_or_404(PostReply, pk=reply_pk, post=post)
    post.replies.update(is_accepted=False)
    reply.is_accepted = True
    reply.save()
    post.status = 'completed'
    post.translated_text = reply.translation
    post.save()
    messages.success(request, 'Reply accepted and post marked as completed!')
    return redirect('post_detail', pk=post_pk)
