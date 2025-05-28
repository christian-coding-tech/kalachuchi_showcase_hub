# your_app/tasks.py
from celery import shared_task
from django.utils import timezone
from .models import TeaserItem, CatalogItem

@shared_task
def move_expired_teasers():
    expired = TeaserItem.objects.filter(expires_at__lt=timezone.now())
    count = expired.count()
    for teaser in expired:
        CatalogItem.objects.create(
            title=teaser.title,
            image=teaser.image,
            description=teaser.description,
            category=teaser.category
        )
        teaser.delete()
    return f"Moved {count} expired teaser(s)."
