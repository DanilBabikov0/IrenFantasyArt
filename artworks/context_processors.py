# artworks/context_processors.py
from .models import Collection
from django.conf import settings


def navigation_context(request):
    try:
        collections = Collection.objects.all()[:5]
        return {
            'collections': collections,
        }
    except:
        return {
            'collections': [],
        }
    
def env_context(request):
    return {
        'TELEGRAM_LINK': settings.TELEGRAM_LINK,
        'TELEGRAM_USERNAME': settings.TELEGRAM_USERNAME,
        'EMAIL_ADDRESS': settings.EMAIL_ADDRESS,
        'PINTEREST_LINK': settings.PINTEREST_LINK,
        'AVITO_LINK': settings.AVITO_LINK,
        'YARMARKA_LINK': settings.YARMARKA_LINK,
        'ADDRESS': settings.ADDRESS,
        'GA_MEASUREMENT_ID': settings.GA_MEASUREMENT_ID,
        'YANDEX_METRICA_ID': settings.YANDEX_METRICA_ID,
    }
