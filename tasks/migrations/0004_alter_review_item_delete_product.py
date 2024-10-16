# Generated by Django 5.0.6 on 2024-10-16 14:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_rename_product_review_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='Item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='tasks.item'),
        ),
        migrations.DeleteModel(
            name='Product',
        ),
    ]