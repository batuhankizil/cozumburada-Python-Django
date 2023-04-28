# Generated by Django 4.1.6 on 2023-04-28 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cozumburada', '0017_alter_complaint_images'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='complaint',
            name='images',
        ),
        migrations.AddField(
            model_name='complaint',
            name='image',
            field=models.ManyToManyField(blank=True, to='cozumburada.image'),
        ),
    ]
