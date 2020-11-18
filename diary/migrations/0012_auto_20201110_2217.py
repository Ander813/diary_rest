# Generated by Django 3.1.3 on 2020-11-10 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0011_auto_20201110_2146'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recordtype',
            name='record_type_parents',
        ),
        migrations.AlterField(
            model_name='recordtype',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.CreateModel(
            name='AbstractRecordType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('entity', models.JSONField()),
                ('children', models.ManyToManyField(related_name='parents', to='diary.RecordType')),
            ],
            options={
                'verbose_name': 'Abstract Record Type',
                'verbose_name_plural': 'Abstract Record Types',
            },
        ),
    ]
