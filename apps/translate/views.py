import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

from AI.main import ai, SUPPORTED_LANGUAGES
from .models import TranslationJob

SUPPORTED_MEDIA_EXTENSIONS = {'.mp3', '.mp4', '.wav', '.m4a', '.ogg', '.webm', '.mov', '.avi'}


def translate_home(request):
    return render(request, 'translate/translate.html', {
        'languages': SUPPORTED_LANGUAGES,
    })


@login_required
def history(request):
    jobs = TranslationJob.objects.filter(user=request.user)
    return render(request, 'translate/history.html', {'jobs': jobs})


@login_required
def job_detail(request, pk):
    job = get_object_or_404(TranslationJob, pk=pk, user=request.user)
    return render(request, 'translate/job_detail.html', {'job': job})


@require_POST
def translate_text_api(request):
    try:
        data = json.loads(request.body)
        text = data.get('text', '').strip()
        target_lang = data.get('target_lang', 'ar')
        source_lang = data.get('source_lang', 'auto')

        if not text:
            return JsonResponse({'success': False, 'error': 'No text provided.'})

        result = ai.translate_text(text, target_lang, source_lang)

        if result['success'] and request.user.is_authenticated:
            TranslationJob.objects.create(
                user=request.user,
                job_type='text',
                source_lang=source_lang,
                target_lang=target_lang,
                original_text=text,
                translated_text=result['translated_text'],
                status='completed',
            )

        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@require_POST
def translate_file_api(request):
    try:
        uploaded = request.FILES.get('file')
        target_lang = request.POST.get('target_lang', 'ar')
        source_lang = request.POST.get('source_lang', 'auto')

        if not uploaded:
            return JsonResponse({'success': False, 'error': 'No file uploaded.'})

        content = uploaded.read()
        result = ai.translate_file(content, uploaded.name, target_lang, source_lang)

        if result['success'] and request.user.is_authenticated:
            TranslationJob.objects.create(
                user=request.user,
                job_type='file',
                source_lang=source_lang,
                target_lang=target_lang,
                original_text=result.get('original_text', ''),
                translated_text=result.get('translated_text', ''),
                status='completed',
            )

        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@require_POST
def translate_video_url_api(request):
    try:
        data = json.loads(request.body)
        video_url = data.get('video_url', '').strip()
        target_lang = data.get('target_lang', 'ar')

        if not video_url:
            return JsonResponse({'success': False, 'error': 'No video URL provided.'})

        result = ai.transcribe_url_then_translate(video_url, target_lang)

        if result['success'] and request.user.is_authenticated:
            TranslationJob.objects.create(
                user=request.user,
                job_type='video_url',
                target_lang=target_lang,
                video_url=video_url,
                transcript=result.get('transcript', ''),
                translated_text=result.get('translated_text', ''),
                status='completed',
            )

        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@require_POST
def translate_video_upload_api(request):
    # Control Variable: Set to True to save the file to Media, False to skip
    SAVE_TO_MEDIA = True 

    try:
        video_file = request.FILES.get('video')
        target_lang = request.POST.get('target_lang', 'ar')

        if not video_file:
            return JsonResponse({'success': False, 'error': 'No video file uploaded.'})

        ext = os.path.splitext(video_file.name)[1].lower()
        if ext not in SUPPORTED_MEDIA_EXTENSIONS:
            return JsonResponse({'success': False, 'error': f'Unsupported format.'})

        # 1. Read the content for the AI (Pointer moves to END)
        content = video_file.read()
        result = ai.transcribe_then_translate(content, video_file.name, target_lang)

        if result['success'] and request.user.is_authenticated:
            # Prepare the data for the database
            job_data = {
                'user': request.user,
                'job_type': 'video_upload',
                'target_lang': target_lang,
                'transcript': result.get('transcript', ''),
                'translated_text': result.get('translated_text', ''),
                'status': 'completed',
            }

            # 2. Check the control variable
            if SAVE_TO_MEDIA:
                # REWIND: Move the file pointer back to the start before saving
                video_file.seek(0)
                job_data['uploaded_file'] = video_file
            
            # Create the record
            TranslationJob.objects.create(**job_data)

        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
