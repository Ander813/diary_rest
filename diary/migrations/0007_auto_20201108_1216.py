# Generated by Django 3.1.3 on 2020-11-08 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0006_auto_20201108_1203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='parents',
            field=models.ManyToManyField(blank=True, related_name='_record_parents_+', to='diary.Record'),
        ),
    ]