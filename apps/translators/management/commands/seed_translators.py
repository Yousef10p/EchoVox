from django.core.management.base import BaseCommand
from apps.translators.models import TranslatorProfile

SAMPLE_TRANSLATORS = [
    {
        "name": "Dr. Aisha Al-Rashid",
        "title": "Legal & Academic Translator",
        "bio": "Over 12 years of experience in legal and academic translation between Arabic and English. Certified by the International Association of Professional Translators. Specializes in contracts, court documents, and scholarly papers.",
        "languages_from": "en", "languages_to": "ar",
        "specialization": "legal", "years_experience": 12,
        "rating": 4.9, "reviews_count": 214, "translations_done": 1840,
        "is_verified": True,
    },
    {
        "name": "Jean-Pierre Moreau",
        "title": "Technical & Business Translator",
        "bio": "Bilingual French-English translator with engineering background. Expert in translating technical manuals, software documentation, and business reports.",
        "languages_from": "en", "languages_to": "fr",
        "specialization": "technical", "years_experience": 8,
        "rating": 4.7, "reviews_count": 98, "translations_done": 723,
        "is_verified": True,
    },
    {
        "name": "Yuki Tanaka",
        "title": "Literary & Marketing Translator",
        "bio": "Japanese-English literary translator with a deep passion for creative writing. Worked with major publishers in Tokyo and New York on novels, manga adaptations, and marketing campaigns.",
        "languages_from": "ja", "languages_to": "en",
        "specialization": "literary", "years_experience": 10,
        "rating": 4.8, "reviews_count": 176, "translations_done": 512,
        "is_verified": True,
    },
    {
        "name": "Maria Santos",
        "title": "Medical & Scientific Translator",
        "bio": "Portuguese-English medical translator with a Master's in Biomedical Sciences. Experienced with clinical trials, patient records, and pharmaceutical documentation.",
        "languages_from": "pt", "languages_to": "en",
        "specialization": "medical", "years_experience": 7,
        "rating": 4.6, "reviews_count": 63, "translations_done": 389,
        "is_verified": False,
    },
    {
        "name": "Klaus Müller",
        "title": "Business & Financial Translator",
        "bio": "German-English business translator with MBA background. Specializes in financial reports, investor documents, and corporate communications for German DAX companies.",
        "languages_from": "de", "languages_to": "en",
        "specialization": "business", "years_experience": 15,
        "rating": 4.9, "reviews_count": 302, "translations_done": 2100,
        "is_verified": True,
    },
    {
        "name": "Sofia Ivanova",
        "title": "General & Academic Translator",
        "bio": "Russian-English translator specializing in academic papers, research, and general content. Holds a PhD in Linguistics from Moscow State University.",
        "languages_from": "ru", "languages_to": "en",
        "specialization": "academic", "years_experience": 9,
        "rating": 4.5, "reviews_count": 87, "translations_done": 641,
        "is_verified": False,
    },
    {
        "name": "Ahmed Hassan",
        "title": "Arabic-English General Translator",
        "bio": "Cairo-based translator with expertise in media, news, and general content translation from Arabic to English. Worked with Al Jazeera and Reuters.",
        "languages_from": "ar", "languages_to": "en",
        "specialization": "general", "years_experience": 6,
        "rating": 4.4, "reviews_count": 55, "translations_done": 298,
        "is_verified": False,
    },
    {
        "name": "Isabella Rossi",
        "title": "Marketing & Creative Translator",
        "bio": "Italian-English creative translator specializing in marketing copy, brand voice, advertising, and cultural adaptation for European markets.",
        "languages_from": "it", "languages_to": "en",
        "specialization": "marketing", "years_experience": 5,
        "rating": 4.6, "reviews_count": 71, "translations_done": 445,
        "is_verified": True,
    },
]


class Command(BaseCommand):
    help = 'Seed the database with sample translator profiles'

    def handle(self, *args, **options):
        count = 0
        for data in SAMPLE_TRANSLATORS:
            _, created = TranslatorProfile.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            if created:
                count += 1
                self.stdout.write(f"  Created: {data['name']}")

        self.stdout.write(self.style.SUCCESS(f'\n✓ Seeded {count} translator profiles.'))
