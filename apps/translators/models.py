from django.db import models
from django.contrib.auth.models import User

LANGUAGE_CHOICES = [
    ('ar', 'Arabic'), ('en', 'English'), ('fr', 'French'),
    ('de', 'German'), ('es', 'Spanish'), ('it', 'Italian'),
    ('pt', 'Portuguese'), ('ru', 'Russian'), ('zh', 'Chinese (Simplified)'),
    ('ja', 'Japanese'), ('ko', 'Korean'), ('tr', 'Turkish'),
    ('nl', 'Dutch'), ('pl', 'Polish'), ('hi', 'Hindi'),
    ('fa', 'Persian'), ('ur', 'Urdu'),
]

CATEGORY_CHOICES = [
    ('legal', 'Legal'), ('medical', 'Medical'), ('technical', 'Technical'),
    ('literary', 'Literary'), ('business', 'Business'), ('marketing', 'Marketing'),
    ('academic', 'Academic'), ('subtitles', 'Subtitles / Captions'),
    ('personal', 'Personal'), ('other', 'Other'),
]

STATUS_CHOICES = [
    ('open', 'Open'), ('in_progress', 'In Progress'), ('completed', 'Completed'),
]


class CommunityPost(models.Model):
    """A user-submitted translation request or shared translation."""
    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title       = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    source_lang = models.CharField(max_length=5, choices=LANGUAGE_CHOICES, default='en')
    target_lang = models.CharField(max_length=5, choices=LANGUAGE_CHOICES, default='ar')
    category    = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    attachment  = models.FileField(upload_to='community/', blank=True, null=True)
    original_text  = models.TextField(blank=True)
    translated_text = models.TextField(blank=True)
    views       = models.PositiveIntegerField(default=0)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def source_lang_name(self):
        return dict(LANGUAGE_CHOICES).get(self.source_lang, self.source_lang)

    @property
    def target_lang_name(self):
        return dict(LANGUAGE_CHOICES).get(self.target_lang, self.target_lang)

    @property
    def reply_count(self):
        return self.replies.count()


class PostReply(models.Model):
    post       = models.ForeignKey(CommunityPost, on_delete=models.CASCADE, related_name='replies')
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    body       = models.TextField()
    translation = models.TextField(blank=True)
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Reply by {self.user.username} on '{self.post.title}'"
