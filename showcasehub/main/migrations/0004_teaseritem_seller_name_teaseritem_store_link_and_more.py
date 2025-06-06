# Generated by Django 5.2.1 on 2025-05-22 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_feedback_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='teaseritem',
            name='seller_name',
            field=models.CharField(default='Unknown Seller', max_length=100),
        ),
        migrations.AddField(
            model_name='teaseritem',
            name='store_link',
            field=models.URLField(default='https://example.com'),
        ),
        migrations.AddField(
            model_name='teaseritem',
            name='store_location',
            field=models.CharField(default='Unknown Location', max_length=200),
        ),
        migrations.AddField(
            model_name='teaseritem',
            name='store_name',
            field=models.CharField(default='Unknown Store', max_length=100),
        ),
    ]
