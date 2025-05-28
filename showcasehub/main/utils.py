from django.utils import timezone
from .models import TeaserItem, CatalogItem

def transfer_expired_teasers():
    expired = TeaserItem.objects.filter(Available__lt=timezone.now())
    for teaser in expired:
        CatalogItem.objects.create(
            title=teaser.title,
            image=teaser.image,
            description=teaser.description,
            category=teaser.category
        )
        teaser.delete()
