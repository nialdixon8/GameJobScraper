# Generated by Django 4.0.2 on 2022-03-28 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameindustry', '0003_technology'),
    ]

    operations = [
        migrations.AddField(
            model_name='technology',
            name='type',
            field=models.CharField(default='TECH', max_length=50),
            preserve_default=False,
        ),
    ]
