# Generated by Django 5.0.2 on 2024-07-15 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0004_alter_category_google_path_alter_category_orig_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.TextField(blank=True, null=True),
        ),
    ]
