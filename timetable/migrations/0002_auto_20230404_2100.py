# Generated by Django 3.2.16 on 2023-04-04 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
        ('timetable', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='My_lecture',
            new_name='MyLecture',
        ),
        migrations.AlterField(
            model_name='review',
            name='content',
            field=models.TextField(),
        ),
    ]
