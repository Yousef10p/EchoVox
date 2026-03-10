from django import forms
from .models import CommunityPost, PostReply, LANGUAGE_CHOICES, CATEGORY_CHOICES


class PostForm(forms.ModelForm):
    title = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Need English → Arabic translation for a legal contract', 'class': 'form-input'}),
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'Add any context, notes, or requirements…', 'class': 'form-input', 'rows': 4}),
    )
    source_lang = forms.ChoiceField(choices=LANGUAGE_CHOICES, widget=forms.Select(attrs={'class': 'form-input'}))
    target_lang = forms.ChoiceField(choices=LANGUAGE_CHOICES, widget=forms.Select(attrs={'class': 'form-input'}))
    category    = forms.ChoiceField(choices=CATEGORY_CHOICES, widget=forms.Select(attrs={'class': 'form-input'}))
    original_text = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'Paste the text you need translated here (optional if uploading a file)…', 'class': 'form-input', 'rows': 6}),
    )
    attachment  = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'form-input'}))

    class Meta:
        model  = CommunityPost
        fields = ('title', 'description', 'source_lang', 'target_lang', 'category', 'original_text', 'attachment')


class ReplyForm(forms.ModelForm):
    body = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Write your comment or translation here…', 'class': 'form-input', 'rows': 4}),
        label='Message',
    )
    translation = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'Paste your translation here (optional)…', 'class': 'form-input', 'rows': 5}),
        label='Translation (optional)',
    )

    class Meta:
        model  = PostReply
        fields = ('body', 'translation')
