# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-09 15:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matchmaker', '0021_add_reader_writer_database_flags'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reader',
            old_name='baseline_wellbeing_email_sent',
            new_name='baseline_survey_email_sent',
        ),
    ]
