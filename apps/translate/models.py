from django.db import models
from django.contrib.auth.models import User

TRANSLATION_TYPES = [
    ('text', 'Text Translation'),
    ('file', 'File Translation'),
    ('video_url', 'Video URL'),
    ('video_upload', 'Video Upload'),
]

LANGUAGE_NAMES = {
    'ar': 'Arabic', 'en': 'English', 'fr': 'French', 'de': 'German',
    'es': 'Spanish', 'it': 'Italian', 'pt': 'Portuguese', 'ru': 'Russian',
    'zh': 'Chinese', 'ja': 'Japanese', 'ko': 'Korean', 'tr': 'Turkish',
    'nl': 'Dutch', 'pl': 'Polish', 'hi': 'Hindi', 'fa': 'Persian', 'ur': 'Urdu',
    'auto': 'Auto',
}


class TranslationJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='translations')
    job_type = models.CharField(max_length=20, choices=TRANSLATION_TYPES, default='text')
    source_lang = models.CharField(max_length=5, default='auto')
    target_lang = models.CharField(max_length=5, default='ar')
    original_text = models.TextField(blank=True)
    transcript = models.TextField(blank=True)
    translated_text = models.TextField(blank=True)
    video_url = models.URLField(blank=True)
    uploaded_file = models.FileField(upload_to='uploads/', blank=True, null=True)
    status = models.CharField(max_length=20, default='completed')
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_job_type_display()} → {self.target_lang} ({self.created_at.strftime('%Y-%m-%d')})"

    @property
    def source_lang_name(self):
        return LANGUAGE_NAMES.get(self.source_lang, self.source_lang.upper())

    @property
    def target_lang_name(self):
        return LANGUAGE_NAMES.get(self.target_lang, self.target_lang.upper())

    @property
    def preview(self):
        text = self.original_text or self.transcript
        return (text[:120] + '…') if len(text) > 120 else text

    @property
    def type_icon(self):
        icons = {'text': '✎', 'file': '📄', 'video_url': '🔗', 'video_upload': '🎬'}
        return icons.get(self.job_type, '✎')
