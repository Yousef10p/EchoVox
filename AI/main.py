"""
LinguaFlow AI Engine
Handles all AI-powered translation and transcription tasks.
"""

import os
import json
import tempfile
import requests
from pathlib import Path
from dotenv import load_dotenv
import yt_dlp
from django.conf import settings
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
ASSEMBLY_AI_KEY = os.getenv("ASSEMBLY_AI_KEY", "")

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_WHISPER_URL = "https://api.groq.com/openai/v1/audio/transcriptions"
ASSEMBLY_AI_TRANSCRIPT_URL = "https://api.assemblyai.com/v2/transcript"
ASSEMBLY_AI_UPLOAD_URL = "https://api.assemblyai.com/v2/upload"

SUPPORTED_LANGUAGES = {
    "ar": "Arabic",
    "en": "English",
    "fr": "French",
    "es": "Spanish",
    "it": "Italian",
    "ru": "Russian",
    "zh": "Chinese (Simplified)",
    "ja": "Japanese",
    "nl": "Dutch",
}


class LinguaFlowAI:
    """
    Central AI class for LinguaFlow translation platform.
    Handles:
    - Text/document translation via Groq LLM
    - Audio/video transcription via Groq Whisper
    - Video URL processing via AssemblyAI
    - Multi-language support
    """

    def __init__(self):
        self.groq_key = GROQ_API_KEY
        self.assembly_key = ASSEMBLY_AI_KEY
        self.groq_headers = {
            "Authorization": f"Bearer {self.groq_key}",
            "Content-Type": "application/json",
        }
        self.assembly_headers = {
            "authorization": self.assembly_key,
            "content-type": "application/json",
        }

    # ── Translation ──────────────────────────────────────────────────────────

    def translate_text(self, text: str, target_lang: str, source_lang: str = "auto") -> dict:
        """
        Translate plain text using Groq LLaMA.
        Returns: {"success": bool, "translated_text": str, "detected_lang": str, "error": str}
        """
        if not self.groq_key:
            return {"success": False, "error": "Translation API key not configured in .env"}

        lang_name = SUPPORTED_LANGUAGES.get(target_lang, target_lang)
        source_hint = f"from {SUPPORTED_LANGUAGES.get(source_lang, 'auto-detected language')}" if source_lang != "auto" else "from whatever language it is written in"

        system_prompt = (
            "You are a professional translator. Translate the given text accurately and naturally. "
            "Preserve formatting, tone, and meaning. Return ONLY the translated text with no explanations, "
            "no preamble, no notes — just the translation itself."
        )

        user_prompt = f"Translate the following text {source_hint} into {lang_name}:\n\n{text}"

        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.3,
            "max_tokens": 4096,
        }

        try:
            response = requests.post(GROQ_API_URL, headers=self.groq_headers, json=payload, timeout=60)
            response.raise_for_status()
            data = response.json()
            translated = data["choices"][0]["message"]["content"].strip()
            return {"success": True, "translated_text": translated, "detected_lang": source_lang}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": f"API request failed: {str(e)}"}
        except (KeyError, IndexError) as e:
            return {"success": False, "error": f"Unexpected API response: {str(e)}"}

    def translate_file(self, file_content: bytes, filename: str, target_lang: str, source_lang: str = "auto") -> dict:
        """
        Translate content from an uploaded file (.txt, .srt, .vtt, .json, .md).
        Returns same structure as translate_text plus original_text.
        """
        try:
            text = file_content.decode("utf-8")
        except UnicodeDecodeError:
            try:
                text = file_content.decode("latin-1")
            except Exception:
                return {"success": False, "error": "Could not decode file. Please upload a UTF-8 text file."}

        if not text.strip():
            return {"success": False, "error": "File appears to be empty."}

        result = self.translate_text(text, target_lang, source_lang)
        result["original_text"] = text
        result["filename"] = filename
        return result

    # ── Transcription ─────────────────────────────────────────────────────────

    def transcribe_audio(self, audio_bytes: bytes, filename: str = "audio.mp3") -> dict:
        """
        Transcribe audio file using Groq Whisper.
        Returns: {"success": bool, "transcript": str, "error": str}
        """
        if not self.groq_key:
            return {"success": False, "error": "Translation API key not configured in .env"}

        try:
            files = {
                "file": (filename, audio_bytes, "audio/mpeg"),
                "model": (None, "whisper-large-v3"),
                "response_format": (None, "text"),
            }
            headers = {"Authorization": f"Bearer {self.groq_key}"}
            response = requests.post(GROQ_WHISPER_URL, headers=headers, files=files, timeout=120)
            response.raise_for_status()
            transcript = response.text.strip()
            return {"success": True, "transcript": transcript}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": f"Transcription failed: {str(e)}"}

    def transcribe_video_url(self, video_url: str) -> dict:
        """
        Transcribe audio from a video URL using AssemblyAI.
        Returns: {"success": bool, "transcript": str, "error": str}
        """
        if not self.assembly_key:
            return {"success": False, "error": "Video transcription API key not configured in .env"}

        try:
            # Submit transcription job
            payload = {"audio_url": video_url}
            response = requests.post(
                ASSEMBLY_AI_TRANSCRIPT_URL,
                headers=self.assembly_headers,
                json=payload,
                timeout=30,
            )
            response.raise_for_status()
            job_id = response.json()["id"]

            # Poll for completion
            import time
            poll_url = f"{ASSEMBLY_AI_TRANSCRIPT_URL}/{job_id}"
            for _ in range(60):  # up to 5 minutes
                time.sleep(5)
                poll = requests.get(poll_url, headers=self.assembly_headers, timeout=30)
                poll.raise_for_status()
                status = poll.json()["status"]
                if status == "completed":
                    return {"success": True, "transcript": poll.json()["text"]}
                elif status == "error":
                    return {"success": False, "error": poll.json().get("error", "Transcription error")}

            return {"success": False, "error": "Transcription timed out after 5 minutes."}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": f"AssemblyAI request failed: {str(e)}"}



    # ── Combined Pipeline ─────────────────────────────────────────────────────

    def transcribe_then_translate(self, audio_bytes: bytes, filename: str, target_lang: str) -> dict:
        """
        Full pipeline: transcribe audio/video file → translate transcript.
        Returns: {"success": bool, "transcript": str, "translated_text": str, "error": str}
        """
        # Step 1: Transcribe
        transcription = self.transcribe_audio(audio_bytes, filename)
        if not transcription["success"]:
            return transcription

        transcript = transcription["transcript"]

        # Step 2: Translate
        translation = self.translate_text(transcript, target_lang)
        translation["transcript"] = transcript
        return translation

    def transcribe_url_then_translate(self, video_url: str, target_lang: str) -> dict:
        """
        Full pipeline: fetch video URL → transcribe → translate.
        """
        # Step 1: Transcribe from URL
        transcription = self.transcribe_video_url(video_url)
        if not transcription["success"]:
            return transcription

        transcript = transcription["transcript"]

        # Step 2: Translate
        translation = self.translate_text(transcript, target_lang)
        translation["transcript"] = transcript
        return translation

    # ── Helpers ───────────────────────────────────────────────────────────────

    def get_supported_languages(self) -> dict:
        return SUPPORTED_LANGUAGES

    def detect_language(self, text: str) -> dict:
        """Use Groq to detect the language of a text snippet."""
        if not self.groq_key:
            return {"success": False, "error": "Translation API key not configured"}

        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": "Detect the language of the text. Reply with ONLY the ISO 639-1 language code (e.g. 'en', 'ar', 'fr'). Nothing else."},
                {"role": "user", "content": text[:500]},
            ],
            "temperature": 0,
            "max_tokens": 10,
        }
        try:
            response = requests.post(GROQ_API_URL, headers=self.groq_headers, json=payload, timeout=30)
            response.raise_for_status()
            code = response.json()["choices"][0]["message"]["content"].strip().lower()
            return {"success": True, "language_code": code, "language_name": SUPPORTED_LANGUAGES.get(code, code)}
        except Exception as e:
            return {"success": False, "error": str(e)}


# Singleton instance
ai = LinguaFlowAI()
