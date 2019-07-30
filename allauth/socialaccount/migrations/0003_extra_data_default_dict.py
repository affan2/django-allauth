# -*- coding: utf-8 -*-


from django.db import models, migrations
import allauth.socialaccount.fields


class Migration(migrations.Migration):

    dependencies = [
        ('socialaccount', '0002_token_max_lengths'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socialaccount',
            name='extra_data',
            field=allauth.socialaccount.fields.JSONField(default=dict, verbose_name='extra data'),
            preserve_default=True,
        ),
    ]
