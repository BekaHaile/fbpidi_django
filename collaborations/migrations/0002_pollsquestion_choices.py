# Generated by Django 3.1.3 on 2021-01-09 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collaborations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pollsquestion',
            name='choices',
            field=models.ManyToManyField(default='', related_name='choices', to='collaborations.Choices'),
        ),
    ]
