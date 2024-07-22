# Generated by Django 5.0.7 on 2024-07-15 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0002_category_orig_id_alter_category_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='sku',
        ),
        migrations.AddField(
            model_name='product',
            name='is_variant',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='skus',
            field=models.TextField(blank=True, null=True),
        ),
    ]
