# 🌐 Echovox — AI Translation Platform

A full-featured Django translation platform powered by Groq AI.

## Features

- **Text Translation** — Translate any text via Groq LLaMA 3.3 70B
- **File Translation** — Upload .txt, .srt, .vtt, .md files
- **Video Transcription** — Upload video/audio for Groq Whisper transcription + translation
- **Video URL** — Provide a video URL and use AssemblyAI to extract + translate the script
- **Browse Translators** — Rich UI to browse, filter, and contact professional translators
- **Authentication** — Full login/register system

## Project Structure

```
linguaflow/
├── manage.py
├── requirements.txt
├── .env.example           ← Copy to .env and fill in API keys
├── linguaflow/            ← Django project settings
│   ├── settings.py
│   └── urls.py
├── AI/
│   └── main.py            ← All AI functionality (EchovoxAI class)
└── apps/
    ├── templates/
    │   └── base.html       ← Shared base template
    ├── core/               ← Landing page
    ├── accounts/           ← Login / Register
    ├── translators/        ← Browse translators
    └── translate/          ← AI translation interface
```

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

| Key | Source | Used For |
|-----|--------|----------|
| `GROQ_API_KEY` | [console.groq.com](https://console.groq.com) (free) | Text translation + audio transcription |
| `ASSEMBLY_AI_KEY` | [assemblyai.com](https://www.assemblyai.com) (free tier) | Video URL transcription |

### 3. Run migrations

```bash
python manage.py migrate
```

### 4. Seed sample translators

```bash
python manage.py seed_translators
```

### 5. Create admin user (optional)

```bash
python manage.py createsuperuser
```

### 6. Start the server

```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000**

## API Keys (both free tiers available)

### Groq API
- Sign up at https://console.groq.com
- Create an API key in the dashboard
- Free tier: very generous limits
- Used for: LLaMA 3.3 70B translation + Whisper Large v3 transcription

### AssemblyAI
- Sign up at https://www.assemblyai.com
- Get API key from dashboard
- Free tier: 5 hours/month of audio
- Used for: Video URL transcription only

## Translation Modes

### 1. Text Translation
- Paste or type text
- Select source/target language
- Uses Groq LLaMA 3.3 70B

### 2. File Translation
- Upload .txt, .srt, .vtt, .md, .csv
- Preserves formatting
- Uses Groq LLaMA 3.3 70B

### 3. Video URL
- Provide direct video URL
- Uses AssemblyAI to transcribe
- Then translates with Groq

### 4. Video Upload
- Upload .mp3, .mp4, .wav, .m4a, .webm
- Uses Groq Whisper Large v3 to transcribe
- Then translates with Groq LLaMA 3.3

## Supported Languages

Arabic, English, French, German, Spanish, Italian, Portuguese, Russian, Chinese, Japanese, Korean, Turkish, Dutch, Polish, Swedish, Hindi, Persian, Urdu

## Admin

Access the Django admin at `/admin/` to manage translators, users, and translation jobs.
