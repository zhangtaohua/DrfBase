# Generated by Django 5.1.6 on 2025-03-18 07:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dictionary', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='dictionary',
            name='creator',
            field=models.ForeignKey(help_text='creator', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='creator', related_query_name='creator_query', to=settings.AUTH_USER_MODEL, verbose_name='创建人'),
        ),
        migrations.AddField(
            model_name='dictionary',
            name='modifier',
            field=models.ForeignKey(help_text='modifier', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='modifier', related_query_name='modifier_query', to=settings.AUTH_USER_MODEL, verbose_name='修改人'),
        ),
        migrations.AddField(
            model_name='dictionary',
            name='parent',
            field=models.ForeignKey(blank=True, db_constraint=False, help_text='parent', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='sublist', to='dictionary.dictionary', verbose_name='父级'),
        ),
    ]
